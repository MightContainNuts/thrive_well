from typing_extensions import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class SOChatSummary(TypedDict):

    summary: Annotated[str, "Summary of the chat history"]
    mood: Annotated[str, "The mood of the text"]
    keywords: Annotated[list[str], "Keywords used in the text"]


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
