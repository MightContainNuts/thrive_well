from pydantic import BaseModel


class StructuredOutputJournalResponse(BaseModel):
    success: bool
    message: str
    response: str
    keywords: list[str]
