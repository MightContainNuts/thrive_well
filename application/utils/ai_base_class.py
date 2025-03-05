from typing import Optional
from abc import ABC, abstractmethod

AIResponse = str


class AIHandler(ABC):
    @abstractmethod
    def __init__(self):
        self.instructions_journal = """
       You are a helpful assistant focused on the well-being of
       others. Categorize the mood of the text as either "positive",
       "negative" or "neutral". Followed by advice on how to improve
       the mood, written clearly and concisely.
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
