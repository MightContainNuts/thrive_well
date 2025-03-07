from typing_extensions import TypedDict, Annotated


class SOJournal(TypedDict):

    success: Annotated[bool, "Whether the request was successful"]
    ai_response: Annotated[str, "The message returned by the model"]
    mood: Annotated[str, "The mood of the text"]
    keywords: Annotated[list[str], "Keywords used in the text"]
    profile_id: Annotated[str, "The profile ID"]
    timestamp: Annotated[str, "The timestamp of the message"]
