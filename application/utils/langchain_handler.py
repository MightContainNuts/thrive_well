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


class LangGraphHandler:
    def __init__(self, profile_id: str):



        self.profile_id = profile_id
        self.db_handler = DBHandler()

        self.memory = MemorySaver()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_retries=2,
        )

        self.chat_summary = self.db_handler.get_chat_summary_from_db(
            self.profile_id
        )

        self.workflow = self._init_workflow()


    def __repr__(self):
        return f"LangGraphHandler(model={self.llm.model}, profile_id={self.profile_id})"


    def _init_workflow(self):
        """Define the graph workflow for conversation"""
        workflow = StateGraph(state_schema=MessagesState)

        # Add nodes and edges to the graph
        workflow.add_edge(START, "model")
        workflow.add_node("model", self.call_model)

        # Compile with memory persistence
        return workflow.compile(checkpointer=self.memory)

    def call_model(self,state: State):
        prompt_template = ChatPromptTemplate.from_messages(state["messages"])
        response = self.llm.invoke(prompt_template.invoke(state))
        return {"messages": response}


    def process_chat(self, user_query: str):
        """Process user input through the workflow."""
        # System message defining assistant behavior
        system_message = SystemMessage(content="""
        You are a helpful assistant focused on the well-being of others.
        You always provide accurate information and support resources.
        If unsure, ask for clarification or acknowledge uncertainty.
        """)

        config = {"configurable": {"thread_id": self.profile_id}}

        # Create input message
        input_messages = HumanMessage(content=user_query)
        output_message = self.workflow.invoke(
            {"messages": input_messages},config)

        ai_message = output_message["messages"][-1].content
        # Append to memory and construct state

        # Summarize and save the chat
        self.summarize_chat(ai_message, user_query)
        self.save_chat_history()

        # Return the AI's response
        return ai_message


    def summarize_chat(self, ai_message, user_query):
        """Summarize the conversation and analyze mood and keywords."""
        print("Summarizing chat history...")
        print("-----------------------------")

        prompt = f"""
        Append the chat summary
        {self.chat_summary}
        with the query {user_query}
        and AI response {ai_message}
        and create a new summary.
        Keep it concise.
        """
        self.chat_summary = self.llm.invoke(prompt).content



    def save_chat_history(self):
        """Save the conversation to memory for future reference."""
        self.db_handler.write_chat_summary_to_db(
            profile_id=self.profile_id,
            summary=self.chat_summary,
        )
