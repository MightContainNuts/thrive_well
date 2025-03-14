from typing import Sequence, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from typing import Dict, Any
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from application.utils.db_handler import DBHandler

load_dotenv()

class State(TypedDict):
    """Unified state for LangGraph workflow."""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    summary: str
    metadata: Dict[str, Any]


class LangGraphHandler:
    """Handler for chat using LangGraph with MemorySaver."""

    def __init__(self, profile_id: str):
        self.profile_id = profile_id

        # Initialize MemorySaver for persistence
        self.memory = MemorySaver()

        # Configuration with thread ID for state isolation
        self.config = {"configurable": {"thread_id": self.profile_id}}

        # Initialize LLM model
        self.model_name = "gpt-4o-mini"
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.7,
            max_retries=2
        )

        # System prompt
        self.system_prompt = """You are a helpful assistant focused on the well-being of others.
        You always provide accurate information and support resources.
        If unsure, ask for clarification or acknowledge uncertainty."""

        # Load assistant guidelines
        self.guidelines = self._load_guidelines()

        # Build the workflow
        self.workflow = self._build_workflow()

        # Initialize DBHandler
        self.db = DBHandler()

    @staticmethod
    def _load_guidelines():
        """Load assistant guidelines from file."""
        try:
            guidelines_path = Path(__file__).parent.parent / "static" / "files" / "guidelines.json"
            with open(guidelines_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading guidelines: {e}")
            return {
                "prohibited_content": ["harmful content", "illegal activities"],
                "privacy": "Do not share personal information"
            }

    def _build_workflow(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(state_schema=State)

        # Add nodes
        workflow.add_node("validate", self._validate_input)
        workflow.add_node("respond", self._generate_response)
        workflow.add_node("summarize", self._update_summary)
        workflow.add_node("save_summary", self._save_summary_to_db)

        # Add edges between nodes
        workflow.add_edge(START, "validate")
        workflow.add_conditional_edges(
            "validate",
            lambda state: "respond" if state["metadata"].get("is_valid", True) else END
        )
        workflow.add_edge("respond", "summarize")
        workflow.add_edge("summarize", "save_summary")
        workflow.add_edge("save_summary", END)

        # Compile the workflow with MemorySaver
        return workflow.compile(checkpointer=self.memory)

    def _validate_input(self, state: State) -> State:
        """Simplify validation by only checking user input against guidelines."""
        print("Validating Query against guidelines")
        try:
            user_message = state["messages"][
                -1].content  # Get the latest message's content
            validation_prompt = f"""
            using {self.guidelines}, validate {user_message}
            Respond with "valid" if the message conforms to the guidelines, or "invalid" otherwise.
            """

            response = self.llm.invoke([SystemMessage(content=validation_prompt)])
            is_valid = (response.content.strip().lower() == "valid")

            # Update state metadata
            state["metadata"]["is_valid"] = is_valid
            print(f"Query within guidelines: {state['metadata']['is_valid']}")

            # Handle non-valid queries by appending a system message
            if not is_valid:
                content = f"""The message does not conform to the guidelines: (did you mention football?)"""
                state["messages"] += [{"role": "assistant", "content": content}]

            return state
        except Exception as e:
            print(f"Error in input validation: {e}")
            state["metadata"]["is_valid"] = True  # Assume valid on error
            return state

    def _generate_response(self, state: State) -> State:
        """Generate a response from the assistant based on the conversation."""
        print("Generating AI response:")
        try:
            # Pass the messages directly to the LLM
            response = self.llm.invoke(state["messages"])

            # Add the AI response directly to the messages field
            state["messages"] += [{"role": "assistant", "content": response.content}]
            print(f"AI Response: {response.content}")
            return state
        except Exception as e:
            print(f"Error generating response: {e}")
            state["messages"] += [{"role": "assistant",
                                   "content": "I'm having trouble processing your request. Please try again later."}]
            return state

    def _update_summary(self, state: State) -> State:
        """Update the conversation summary."""
        print("Updating Summary:")
        try:
            if len(state["messages"]) >= 3:  # Ensure sufficient history
                recent_messages = state["messages"][-2:]

                # Prepare the prompt for generating a summary
                summary_prompt = f"""Previous summary: {state['summary']}
                New exchange:
                User: {recent_messages[0].content if isinstance(recent_messages[0], HumanMessage) else ''}
                Assistant: {recent_messages[1].content if isinstance(recent_messages[1], AIMessage) else ''}
                Provide a concise summary of the conversation so far."""

                # Use LLM to generate the updated summary
                summary_response = self.llm.invoke([HumanMessage(content=summary_prompt)])
                state["summary"] = summary_response.content
                print(f"Updated Summary: {state['summary']}")
            return state
        except Exception as e:
            print(f"Error updating summary: {e}")
            return state

    def _save_summary_to_db(self, state: State):
        print("Saving chat summary to the database")
        profile_id = self.profile_id
        summary = state["summary"]
        self.db.write_chat_summary_to_db(profile_id, summary)
        print("Chat summary saved to the database.")

    def process_chat(self, user_message: str) -> str:
        """Process user input through the workflow and return the AI's response."""
        try:
            input_state: State = {
                "messages": [HumanMessage(content=user_message)],
                "summary": "",
                "metadata": {"is_valid": True}
            }

            result = self.workflow.invoke(input_state, self.config)

            ai_messages = [msg for msg in result["messages"] if
                           isinstance(msg, AIMessage)]
            return ai_messages[
                -1].content if ai_messages else "No response was generated."
        except Exception as e:
            print(f"Error processing chat: {e}")
            return "An error occurred. Please try again later."


