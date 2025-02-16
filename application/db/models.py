from enum import Enum as PyEnum
import uuid
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from application.db_init import db


class MoodStatus(str, PyEnum):
    VERY_POSITIVE = "very positive"
    SOMEWHAT_POSITIVE = "somewhat positive"
    NEUTRAL = "neutral"
    SOMEWHAT_NEGATIVE = "somewhat negative"
    VERY_NEGATIVE = "very negative"


class RoleStatus(str, PyEnum):
    MODERATOR = "moderator"
    USER = "user"
    ADMIN = "admin"


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    user_name = db.Column(String(64), unique=True)
    email = db.Column(String(100), unique=True)
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())
    role = db.Column(SQLEnum(RoleStatus), default=RoleStatus.USER)
    profile = relationship(
        "Profiles",
        backref=db.backref("user", uselist=False),
        uselist=False,  # noqa E501
    )


class Profiles(db.Model):
    __tablename__ = "profiles"
    profile_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    user_name = db.Column(String(64), unique=True)
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())
    mood = db.Column(SQLEnum(MoodStatus), default=MoodStatus.NEUTRAL)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), unique=True
    )  # noqa E501


class MoodHistory(db.Model):
    __tablename__ = "mood_history"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mood = db.Column(SQLEnum(MoodStatus), default=MoodStatus.NEUTRAL)
    timestamp = db.Column(DateTime, default=func.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"))


class Activity(db.Model):
    __tablename__ = "activities"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    activity_type = db.Column(String(100))
    description = db.Column(String(255))
    timestamp = db.Column(DateTime, default=func.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"))


class Journals(db.Model):
    __tablename__ = "journals"
    journal_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    profile_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("profiles.profile_id")
    )  # noqa E501
    sentiment = db.Column(SQLEnum(MoodStatus), default=MoodStatus.NEUTRAL)
    created_on = db.Column(DateTime, default=func.now())
    profile = db.relationship(
        "Profiles", backref=db.backref("journals", lazy=True)
    )  # noqa E501


class Plans(db.Model):
    __tablename__ = "plans"
    plan_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    profile_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("profiles.profile_id")
    )  # noqa E501
    created_on = db.Column(DateTime, default=func.now())
    profile = db.relationship(
        "Profiles", backref=db.backref("plans", lazy=True)
    )  # noqa E501
