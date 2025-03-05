from typing import override, Optional
from flask.cli import load_dotenv

import anthropic
import os
from application.utils.ai_base_class import AIHandler, AIResponse


load_dotenv()


class AnthropicAIHandler(AIHandler):
    def __init__(self):
        print(os.getenv("ANTHROPIC_API_KEY"))
        self.anthropic = anthropic.Anthropic()
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

    @override
    def create_google_search_query(
        self, key_words: str
    ) -> Optional[AIResponse | None]:  # noqa E501
        pass

    @override
    def create_journal_entry_response(
        self, journal_entry: str
    ) -> Optional[AIResponse | None]:
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": journal_entry},
            ],
        )
        return response.text
