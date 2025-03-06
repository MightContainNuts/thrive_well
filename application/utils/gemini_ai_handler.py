from flask.cli import load_dotenv
from google import genai
from google.genai import types

from application.utils.structured_outputs import (
    StructuredOutputJournalResponse,
)  # noqa E501
import os
from typing import Optional, override
from application.utils.ai_base_class import AIHandler, AIResponse

load_dotenv()


class GeminiAIHandler(AIHandler):
    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    @override
    def create_journal_entry_response(self, journal_entry: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=journal_entry,
            config=types.GenerateContentConfig(
                system_instruction=self.instructions_journal,
                response_mime_type="application/json",
                response_schema=StructuredOutputJournalResponse,
            ),
        )
        return response.text

    @override
    def create_google_search_query(
        self, google_search: str
    ) -> Optional[AIResponse | None]:
        pass
