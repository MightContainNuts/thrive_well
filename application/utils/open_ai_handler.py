from flask.cli import load_dotenv
from application.utils.structured_outputs import (
    StructuredOutputJournalResponse,
)  # noqa E501
from openai import OpenAI
import os
from typing import Dict, Any, Optional

load_dotenv()
AIResponse = Dict[str, Any]


class OpenAIHandler:
    def __init__(self):
        self.client = OpenAI()
        self.MODEL = "gpt-4o-mini"
        self.client.api_key = os.environ.get("OPENAI_API_KEY")

    def create_google_search_query(self, key_words: str) -> str:
        content = """
                You want to help someone find the best information on the web
                 to help someone and improve their quality of life. The
                 returned google search query should be a string that can be
                 used to search for websites offering tips, tricks, help to
                 maximum effectiveness
                """
        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": f"{key_words}"},
            ],
        )
        response = completion.choices[0].message.content
        return response

    def create_journal_entry_response(
        self, journal_entry: str
    ) -> Optional[AIResponse | None]:
        """create_journal_entry_response using open AI"""
        content = """
                You are a helpful assistant focused on the well-being of
                others. Categorize the mood of the text as either "positive",
                "negative" or "neutral". Followed by advice on how to improve
                the mood, written clearly and concisely.
                """
        completion = self.client.beta.chat.completions.parse(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": content},
                {"role": "user", "content": journal_entry},
            ],
            response_format=StructuredOutputJournalResponse,
        )
        response = completion.choices[0].message.content
        print(response)

        return response
