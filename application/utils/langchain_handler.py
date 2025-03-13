import os

from dotenv import load_dotenv
from langchain.chains.summarize.refine_prompts import prompt_template
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_community.chat_message_histories import ChatMessageHistory
from application.utils.structured_outputs import State

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
        self.chat_summary = self.db_handler.get_chat_summary_from_db(
            self.profile_id
        )
        self.memory = ChatMessageHistory()

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
        def call_model(state: State):
            prompt = prompt_template.invoke(state)
            response = self.llm.invoke(prompt)
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

    def process_chat(self, user_query: str) -> AIResponse:
        """Analyze journal entry using LangChain with chat history"""

        content = """
        You are a helpful assistant focused on the well-being of
        others. Ypu always give accurate information and provide information
        on how to help others. Especially if you notice a negative mood.
        If you do not understand, ask for clarification or more context
        and if you do not know the answer, say so.
        """
        system_message = SystemMessage(content=content)
        config = {"configurable": {"profile_id": self.profile_id}}

        human_message = HumanMessage(user_query)
        prompt = ChatPromptTemplate.from_messages(
            messages=[
                system_message,
                MessagesPlaceholder(variable_name="messages"),
                human_message,
            ]
        )
        state = {
            "messages": self.memory.messages,
        }
        chain = prompt | self.llm
        ai_msg = chain.invoke(state, config=config)

        self.memory.add_user_message(user_query)
        self.memory.add_ai_message(ai_msg.content)

        self.summarize_chat()
        self.save_chat_history()

        return ai_msg.content

    def update_chat_history(self, entry: dict):
        self.chat_history.append(entry)

    def summarize_chat(self):
        """Summarize the conversation and analyze mood and keywords."""

        chat_text = "\n".join(
            [entry.content for entry in self.memory.messages]
        )
        if not self.chat_summary:
            self.chat_summary = ""
        self.chat_summary += chat_text
        prompt = f"""
        Summarize the following conversation:
        {self.chat_summary}\n\n
        Keep it concise.
        """

        response = self.llm.invoke([SystemMessage(content=prompt)])
        self.chat_summary = response.content.strip()
        return self.memory

    def save_chat_history(self):
        """Save the conversation to memory for future reference."""
        self.db_handler.write_chat_summary_to_db(
            profile_id=self.profile_id,
            summary=self.chat_summary,
        )
