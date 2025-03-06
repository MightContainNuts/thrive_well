from pydantic import BaseModel


class StructuredOutputJournalResponse(BaseModel):
    success: bool
    advice: str
    mood: str
    keywords: list[str]
