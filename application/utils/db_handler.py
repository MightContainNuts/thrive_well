from datetime import datetime
from typing import Optional, Union

from application.db.models import (
    User,
    Profile,
    Journal,
    ChatSummary,
)
from application.utils.extensions import db

dt = datetime.now()
formatted_dt = dt.strftime("%Y-%m-%d %H:%M")
AI_RESPONSE = dict[str, Optional[Union[str, list[str]]]]


class DBHandler:
    def __init__(self):
        self.db = db
        self.User = User
        self.Profile = Profile
        self.Journal = Journal
        self.ChatSummary = ChatSummary

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

    def write_chat_summary_to_db(
        self,
        profile_id: str,
        summary: str,
    ) -> None:
        """Write a chat message to the chat history table."""

        chat_history = self.ChatSummary(
            profile_id=profile_id,
            summary=summary,
            timestamp=formatted_dt,
        )
        print(f"chat_history: {profile_id}:")
        print("-"*50)
        print(summary)
        print("-"*50)

        self.add_and_commit(chat_history)

    def get_chat_summary_from_db(
        self, profile_id: str
    ) -> Optional[str | None]:
        """Get chat history from the database."""
        chat_summary = self.ChatSummary.query.filter_by(
            profile_id=profile_id
        ).first()
        if chat_summary:
            return chat_summary.summary
