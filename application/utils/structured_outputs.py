from typing_extensions import TypedDict, Annotated


class SOChatSummary(TypedDict):

    summary: Annotated[str, "Summary of the chat history"]
    mood: Annotated[str, "The mood of the text"]
    keywords: Annotated[list[str], "Keywords used in the text"]
