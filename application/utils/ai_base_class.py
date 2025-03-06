from typing import Optional
from abc import ABC, abstractmethod

AIResponse = str


class AIHandler(ABC):
    @abstractmethod
    def __init__(self):
        self.instructions_journal = """
You are a well-being assistant focused on helping users reflect on their
emotions.
- Categorize the mood of the text as **"positive"**, **"negative"**, or
**"neutral"**.
- Provide **clear and concise advice** on how to improve the mood if necessary.
- Ensure your response is **supportive, encouraging, and actionable**.
"""

    @abstractmethod
    def create_google_search_query(
        self, key_words: str
    ) -> Optional[AIResponse | None]:  # noqa E501
        pass

    @abstractmethod
    def create_journal_entry_response(
        self, journal_entry: str
    ) -> Optional[AIResponse | None]:
        pass
