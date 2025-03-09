from typing_extensions import TypedDict, Annotated


class SOChat(TypedDict):

    success: Annotated[bool, "Whether the request was successful"]
    ai_response: Annotated[str, "The message returned by the model"]
    mood: Annotated[str, "The mood of the text"]
    keywords: Annotated[list[str], "Keywords used in the text"]
