from typing_extensions import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class SOChatSummary(BaseModel):

    summary: Annotated[str, "Summary of the chat history"]
    mood: Annotated[str, "The mood of the text"]
    keywords: Annotated[list[str], "Keywords used in the text"]


class State(BaseModel):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class AssistantGuidelines(BaseModel):
    is_within_guidelines: Annotated[bool, "Query conforms with guidelines"]

