from flask.cli import load_dotenv
from openai import OpenAI
import os
from typing import Optional, override
from application.utils.ai_base_class import AIHandler, AIResponse

load_dotenv()


class OpenAIHandler(AIHandler):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()
        self.MODEL = "gpt-4o-mini"
        self.client.api_key = os.environ.get("OPENAI_API_KEY")

    @override
    def create_google_search_query(self, key_words: str) -> str:

        completion = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.instructions_journal},
                {"role": "user", "content": f"{key_words}"},
            ],
        )
        response = completion.choices[0].message.content
        return response

    @override
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
        )
        structured_response = completion.choices[0].message.parsed

        json_response = structured_response.model_dump_json(indent=4)

        return json_response
