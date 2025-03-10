from application.utils.extensions import db
from application.db.models import (
    User,
    Profile,
    Journal,
    Medications,
    ChatHistory,
)
from datetime import datetime
from typing import Optional, Union, List


dt = datetime.now()
formatted_dt = dt.strftime("%Y-%m-%d %H:%M")
AI_RESPONSE = dict[str, Optional[Union[str, list[str]]]]


class DBHandler:
    def __init__(self):
        self.db = db
        self.User = User
        self.Profile = Profile
        self.Journal = Journal
        self.Medications = Medications
        self.ChatHistory = ChatHistory

    def add_and_commit(self, obj):
        """Add and commit an object to the database."""
        try:
            self.db.session.add(obj)
            self.db.session.commit()
            print(f"Successfully added {obj} to the database.")
        except Exception as e:
            self.db.session.rollback()
            return str(e)

    def add_journal_entry(
        self, profile_id: str, entry: str, ai_response: AI_RESPONSE
    ) -> None:  # noqa E501
        """Add a journal entry to the database."""
        journal_entry = self.Journal(
            profile_id=profile_id,
            entry=entry,
            created_on=formatted_dt,
            ai_response=ai_response,
        )
        self.add_and_commit(journal_entry)

    def write_chat_message_to_db(
        self,
        profile_id: str,
        summary: str,
        mood: str,
        embedded_chunk: str,
        keywords: List[str],
    ) -> None:
        """Write a chat message to the chat history table."""

        chat_history = self.ChatHistory(
            profile_id=profile_id,
            summary=summary,
            mood=mood,
            embedded_chunk=embedded_chunk,
            keywords=keywords,
            timestamp=formatted_dt,
        )
        print(chat_history)
        self.add_and_commit(chat_history)

    def get_chat_history(self, profile_id: str) -> str:
        """Get chat history from the database."""
        chat_str = ""
        chat_history = self.ChatHistory.query.filter_by(
            profile_id=profile_id
        ).all()
        for chat in chat_history:
            chat_str += f"USER: {chat.user_query}\n BOT: {chat.ai_response} \n"
        return chat_str
