import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from application.utils.structured_outputs import SOChat
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


# from application.utils.structured_outputs import SOChat

from typing_extensions import TypedDict
from application.utils.db_handler import DBHandler

# from application.app import app

# from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
)

AIResponse = TypedDict
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
            response = self.model.invoke(state["messages"])
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

    def chatbot(self, user_query: str) -> AIResponse:
        """Analyze journal entry using LangChain with chat history"""

        # Define initial system message
        content = """
        You are a helpful assistant focused on the well-being of
        others. Categorize the following:
        - success of the request as either True or False
        - mood of the text as either "positive", "negative" or "neutral".
        - the ai_response as the response
        - Summarise the keywords used in the text and response.
        If you do not understand anything, ask for clarification
        and if you do not know the answer,
        say so.
        """
        system_message = SystemMessage(content=content)

        # Fetch conversation history (if available)
        conversation_history = self.get_conversation_history()

        # Build the message prompt with history
        history_messages = [
            HumanMessage(content=entry["message"])
            if entry["sender"] == "user"
            else SystemMessage(content=entry["message"])
            for entry in conversation_history
        ]
        human_message = HumanMessage(content=user_query)
        prompt = ChatPromptTemplate(
            messages=[
                system_message,
                *history_messages,  # Add conversation history
                human_message,  # Add the new user message
            ]
        )

        # Pass the prompt to the LangChain model
        chain = prompt | self.llm.with_structured_output(SOChat)
        ai_msg = chain.invoke({})

        # Extract and log metadata from AI response
        mood = ai_msg["mood"]
        keywords = ai_msg["keywords"]
        success = ai_msg["success"]
        ai_response = ai_msg["ai_response"]

        # Print logs for debugging
        print(f"success: {success}")
        print(f"mood: {mood}")
        print(f"keywords: {keywords}")
        print(f"user_query: {user_query}")
        print(f"ai_response: {ai_response}")
        print(f"profile_id: {self.profile_id}")

        # Update chat history with user message and AI response
        self.update_chat_history({"sender": "user", "message": user_query})
        self.update_chat_history({"sender": "ai", "message": ai_response})

        return ai_msg

    def get_conversation_history(self):
        """Retrieve conversation history"""
        return self.chat_history

    def update_chat_history(self, entry: dict):
        """Update chat history with a new message"""
        self.chat_history.append(entry)
