from pydantic import BaseModel


class StructuredOutputJournalResponse(BaseModel):
    success: bool
    message: str
    mood: str
    keywords: list[str]
