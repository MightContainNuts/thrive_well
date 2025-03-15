from typing import Sequence, Annotated, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from application.langgraph_interface.tools.open_weather_map_tool import (
    get_weather,
)
from application.langgraph_interface.tools.wikipedia_tool import (
    get_wiki_summary,
)
from application.langgraph_interface.tools.tavily_search_tool import (
    get_tavily_search_tool,
)
from application.utils.db_handler import DBHandler
from langgraph.prebuilt import create_react_agent
import uuid

load_dotenv()


# Define the state type with proper annotations
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
        self.in_memory_vector_store = InMemoryVectorStore(OpenAIEmbeddings())

        # Configuration with thread ID for state isolation
        thread_id = str(uuid.uuid4())
        self.config = {
            "configurable": {
                "user_id": self.profile_id,
                "thread_id": thread_id,
            }
        }

        # Initialize LLM model
        self.model_name = "gpt-4o-mini"
        self.llm = ChatOpenAI(
            model=self.model_name, temperature=0.7, max_retries=2
        )

        # System prompt
        self.system_prompt = """You are a helpful assistant focused on the
        well-being of others. You always provide accurate information and
        support resources.If unsure, ask for clarification or acknowledge
        uncertainty."""

        # Load assistant guidelines
        self.guidelines = self._load_guidelines()

        # Initialize DBHandler
        self.db = DBHandler()

        # Load summary
        self.summary = self.db.get_chat_summary_from_db(profile_id) or ""

        # Define available tools
        self.tools = [get_weather, get_wiki_summary, get_tavily_search_tool]

        # Build the workflow
        self.workflow = self._build_workflow()

    @staticmethod
    def _load_guidelines():
        """Load assistant guidelines from file."""
        try:
            guidelines_path = (
                Path(__file__).parent.parent
                / "static"
                / "files"
                / "guidelines.json"
            )
            with open(guidelines_path, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading guidelines: {e}")
            return {
                "prohibited_content": [
                    "harmful content",
                    "illegal activities",
                ],
                "privacy": "Do not share personal information",
            }

    def _build_workflow(self):
        """Build the LangGraph workflow."""
        workflow = StateGraph(State)

        # Create the agent node with the ReAct agent
        agent = create_react_agent(
            self.llm,
            self.tools,
        )

        # Add nodes to the graph
        workflow.add_node("validate", self._validate_input)
        workflow.add_node("agent", agent)
        workflow.add_node("summarize", self._update_summary)
        workflow.add_node("save_summary", self._save_summary_to_db)

        # Add edges between nodes
        workflow.add_edge(START, "validate")
        workflow.add_conditional_edges(
            "validate",
            lambda state: "agent"
            if state["metadata"].get("is_valid", True)
            else END,
        )
        workflow.add_edge("agent", "summarize")
        workflow.add_edge("summarize", "save_summary")
        workflow.add_edge("save_summary", END)

        # Compile the workflow with MemorySaver
        return workflow.compile(checkpointer=self.memory)

    def _validate_input(self, state: State) -> State:
        """Validate user input against guidelines."""
        print("Validating Query against guidelines")
        try:
            user_message = state["messages"][-1].content
            validation_prompt = f"""Using {self.guidelines},
            validate '{user_message}' Respond with "valid" if the message
            conforms to the guidelines, or "invalid" otherwise."""

            response = self.llm.invoke(
                [SystemMessage(content=validation_prompt)]
            )
            is_valid = response.content.strip().lower() == "valid"

            # Update state metadata
            state["metadata"]["is_valid"] = is_valid
            print(f"Query within guidelines: {state['metadata']['is_valid']}")

            # Handle non-valid queries
            if not is_valid:
                # When using add_messages annotation, we should return a new
                # message to be added to the state rather than modifying state
                # directly
                return {
                    "messages": [
                        AIMessage(
                            content="""The message does not conform to the guidelines # noqa E501
                            (did you mention football?)"""
                        )
                    ],
                    "summary": state["summary"],
                    "metadata": state["metadata"],
                }
            return state
        except Exception as e:
            print(f"Error in input validation: {e}")
            state["metadata"]["is_valid"] = True  # Assume valid on error
            return state

    def _update_summary(self, state: State) -> State:
        """Update the conversation summary."""
        print("Updating Summary:")
        try:
            if len(state["messages"]) >= 2:  # Ensure sufficient history
                # Get the most recent user and assistant messages
                recent_messages = state["messages"][-2:]

                # Format the messages for the summary prompt
                user_msg = ""
                ai_msg = ""
                for msg in recent_messages:
                    if isinstance(msg, HumanMessage):
                        user_msg = msg.content
                    elif isinstance(msg, AIMessage):
                        ai_msg = msg.content

                # Create a summary prompt for the LLM
                summary_prompt = f"""
                Previous summary: {state["summary"]}

                New exchange:
                User: {user_msg}
                Assistant: {ai_msg}

                Provide a concise summary of the entire conversation so far.
                """

                # Generate new summary
                summary_response = self.llm.invoke(
                    [HumanMessage(content=summary_prompt)]
                )

                # Return the updated state with the new summary
                return {
                    "messages": state["messages"],
                    "summary": summary_response.content,
                    "metadata": state["metadata"],
                }
            return state
        except Exception as e:
            print(f"Error updating summary: {e}")
            return state

    def _save_summary_to_db(self, state: State) -> State:
        """Save the summary to the database."""
        print("Saving chat summary to the database")
        try:
            self.db.write_chat_summary_to_db(self.profile_id, state["summary"])
            print("Chat summary saved to the database.")
        except Exception as e:
            print(f"Error saving summary to database: {e}")
        return state

    def process_chat(self, user_message: str) -> str:
        """Process user input through workflow and return the AI's response."""
        try:
            # Create initial state
            input_state: State = {
                "messages": [HumanMessage(content=user_message)],
                "summary": self.summary,  # Use existing summary
                "metadata": {"is_valid": True},
            }

            # Invoke the workflow
            result = self.workflow.invoke(input_state, self.config)

            # Extract AI response
            ai_messages = [
                msg.content
                for msg in result["messages"]
                if isinstance(msg, AIMessage)
            ]
            return (
                ai_messages[-1]
                if ai_messages
                else "No response was generated."
            )
        except Exception as e:
            print(f"Error processing chat: {e}")
            return "An error occurred. Please try again later."
