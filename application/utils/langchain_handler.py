import os
import time
import threading
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from application.utils.structured_outputs import SOChatSummary
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.prompts import PromptTemplate
from nltk.tokenize import word_tokenize

from sentence_transformers import SentenceTransformer
from typing_extensions import TypedDict
from application.utils.db_handler import DBHandler
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
)

AIResponse = str
Summary = TypedDict(
    "Summary", {"summary": str, "mood": str, "keywords": list[str]}
)
load_dotenv()


class LangChainHandler:
    def __init__(self, profile_id: str):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.temperature = 0.7
        self.max_retries = 2
        self.profile_id = profile_id
        self.db_handler = DBHandler()
        self.memory = MemorySaver()
        self.llm = self.init_model()
        self.workflow = self._init_workflow()
        self.chat_history = []
        self.timer = None
        self.inactivity_timeout = 30
        self.last_message_time = time.time()

    def __repr__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries}),"
            f"profile_id={self.profile_id}"
        )

    def __str__(self):
        return (
            f"LangChainHandler(model={self.model}, "
            f"temperature={self.temperature}, "
            f"max_retries={self.max_retries}),"
            f"profile_id={self.profile_id}"
        )

    def _init_workflow(self):
        """Define the graph workflow for conversation"""
        workflow = StateGraph(state_schema=MessagesState)

        # Define the function that calls the model
        def call_model(state: MessagesState):
            response = self.llm.invoke(state["messages"])
            return {"messages": response}  # Append new messages

        # Add nodes and edges to the graph
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        # Compile with memory persistence
        return workflow.compile(checkpointer=self.memory)

    def init_model(self):
        """initialise chat model"""
        return ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_retries=self.max_retries,
        )

    def start_inactivity_timer(self) -> None:
        """Start a timer that triggers saving chat history if inactive."""
        self.timer = threading.Timer(
            self.inactivity_timeout, self.store_chat_history_to_db
        )
        self.timer.start()

    def chatbot(self, user_query: str) -> AIResponse:
        self.last_message_time = time.time()
        if self.timer:
            self.timer.cancel()

        response = self.process_chat(user_query)

        self.start_inactivity_timer()
        return response

    def process_chat(self, user_query: str) -> AIResponse:
        """Analyze journal entry using LangChain with chat history"""

        # Define initial system message
        content = """
        You are a helpful assistant focused on the well-being of
        others. Ypu always give accurate information and provide information
        on how to help others. Especially if you notice a negative mood.
        If you do not understand, ask for clarification or more context
        and if you do not know the answer, say so.
        """
        system_message = SystemMessage(content=content)

        history_messages = [
            HumanMessage(content=entry["message"])
            if entry["sender"] == "user"
            else SystemMessage(content=entry["message"])
            for entry in self.chat_history
        ]
        human_message = HumanMessage(content=user_query)
        prompt = ChatPromptTemplate(
            messages=[
                system_message,
                *history_messages,
                human_message,
            ]
        )

        chain = prompt | self.llm
        ai_msg = chain.invoke({})

        self.update_chat_history({"sender": "user", "message": user_query})
        self.update_chat_history({"sender": "ai", "message": ai_msg.content})
        print(self.chat_history)

        return ai_msg.content

    def update_chat_history(self, entry: dict):
        self.chat_history.append(entry)

    def summarize_chat(self) -> Summary:
        """Generate a summary of the chat session."""
        prompt = PromptTemplate(
            input_variables=["chat"],
            template="""
            Summarize the following conversation:
            {chat}\n\nKeep it concise.""",
        )
        messages = [
            SystemMessage(
                content="""
                You are a helpful assistant that summarizes conversations."""
            ),
            HumanMessage(
                content=prompt.format(
                    chat="\n".join(
                        entry["message"] for entry in self.chat_history
                    )
                )
            ),
        ]
        response = self.llm.with_structured_output(SOChatSummary).invoke(
            messages
        )
        print(f"Summary (TimeOut): {response}")
        return response

    def save_chat_history(self):
        print("Saving chat history")
        assert self.chat_history

    def chunk_chat_history(self, messages, max_tokens=512):
        """Chunk the chat history into smaller pieces."""
        chunks = []
        current_chunk = []
        current_tokens = 0

        for msg in messages:
            msg_tokens = len(msg)  # Get token count

            if current_tokens + msg_tokens > max_tokens:
                # Store current chunk if limit exceeded
                chunks.append(" ".join(current_chunk))
                current_chunk = []  # Start a new chunk
                current_tokens = 0

            current_chunk.append(msg)
            current_tokens += msg_tokens

        # Add last chunk if not empty
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def create_embedding_vector(self, chunk: str) -> str:
        """Create an embedding vector for the chat history."""
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model.encode(chunk)

    def tokenize_text(self, text: str) -> list:
        """Tokenize the text into words."""
        return word_tokenize(text)

    def store_chat_history_to_db(self) -> None:
        """Store the chat history in the database."""
        summary = self.summarize_chat()
        summary_text = summary["summary"]
        summary_keywords = summary["keywords"]
        summary_mood = summary["mood"]
        chunks = self.chunk_chat_history(summary)
        for chunk in chunks:
            embedded_chunk = self.create_embedding_vector(chunk)
            self.db_handler.write_chat_message_to_db(
                profile_id=self.profile_id,
                summary=summary_text,
                mood=summary_mood,
                embedded_chunk=embedded_chunk,
                keywords=summary_keywords,
            )
