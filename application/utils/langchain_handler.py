import os
import json

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from application.utils.structured_outputs import State, AssistantGuidelines

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
        self.model = "gpt-4o-mini"

        self.memory = MemorySaver()
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0.7,
            max_retries=2,
        )

        self.chat_summary = self.db_handler.get_chat_summary_from_db(
            self.profile_id
        )

        self.workflow = self._init_workflow()


    def __repr__(self):
        return f"LangGraphHandler(model={self.model}, profile_id={self.profile_id})"


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
        self._summarize_chat(ai_message, user_query)
        self._save_chat_history()

        # Return the AI's response
        return ai_message

    def is_user_query_valid(self, user_query: str) -> bool:
        """Check if the user query is valid and doesn't go against the
        assistant's guidelines."""

        GUIDELINES = self._load_guidelines()
        system_message = SystemMessage(content="""
        You are an ethical assistant that follows the guidelines set
        down in {GUIDELINES}.
        Evaluate the user query and determine if it is within the guidelines.
        """)

        inputs = {
            "system_message": system_message,
            "user_query": user_query,
        }
        output = self.workflow.invoke(inputs).with_structured_outputs(AssistantGuidelines)
        print(output)



    def _load_guidelines(self):
        """Load the guidelines for the assistant."""
        with open("assistant_guidelines.json", "r") as file:
            return json.load(file)

    def _summarize_chat(self, ai_message, user_query):
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


    def _save_chat_history(self):
        """Save the conversation to memory for future reference."""
        self.db_handler.write_chat_summary_to_db(
            profile_id=self.profile_id,
            summary=self.chat_summary,
        )

