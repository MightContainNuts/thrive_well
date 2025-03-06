from typing import override, Optional
from flask.cli import load_dotenv
from groq import Groq
from application.utils.structured_outputs import (
    StructuredOutputJournalResponse,
)  # noqa E501
import json
import os
from application.utils.ai_base_class import AIHandler, AIResponse


load_dotenv()


class GroqAIHandler(AIHandler):
    def __init__(self):
        super().__init__()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        self.journal_tool = [
            {
                "type": "function",
                "function": {
                    "name": "get_journal_entry_response",
                    "description": "Processes a journal entry and extracts key insights.",  # noqa E501
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean"},
                            "advice": {"type": "string"},
                            "mood": {"type": "string"},
                            "keywords": {
                                "type": "array",
                                "items": {"type": "string"},
                            },  # noqa E501
                        },
                        "required": ["success", "message", "mood", "keywords"],
                    },
                },
            }
        ]

    @override
    def create_google_search_query(
        self, key_words: str
    ) -> Optional[AIResponse | None]:  # noqa E501
        pass

    @override
    def create_journal_entry_response(
        self, journal_entry: str
    ) -> StructuredOutputJournalResponse:
        chat_completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": self.instructions_journal},
                {"role": "user", "content": journal_entry},
            ],
            tools=self.journal_tool,
            tool_choice={
                "type": "function",
                "function": {"name": "get_journal_entry_response"},
            },
        )

        tool_calls = chat_completion.choices[0].message.tool_calls
        if not tool_calls:
            raise ValueError("No tool call response found!")
        function_response = tool_calls[0].function.arguments
        parsed_data = json.loads(function_response)
        return StructuredOutputJournalResponse(**parsed_data)
