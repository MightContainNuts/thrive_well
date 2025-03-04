from application.db_init import db
from application.db.models import User, Profile, Journal, Medications
from datetime import datetime
from typing import Optional, Union


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

    def add_and_commit(self, obj):
        """Add and commit an object to the database."""
        try:
            self.db.session.add(obj)
            self.db.session.commit()
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
