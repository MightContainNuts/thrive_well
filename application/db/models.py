from enum import Enum as PyEnum
import uuid


from sqlalchemy import Enum as SQLEnum, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from pgvector.sqlalchemy import Vector



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


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    user_name = db.Column(String(64), unique=True)
    email = db.Column(String(100), unique=True)
    password_hash = db.Column(String(256))
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())
    role = db.Column(SQLEnum(RoleStatus), default=RoleStatus.USER)
    profile = relationship(
        "Profile",
        backref=db.backref("user", uselist=False),
        uselist=False,  # noqa E501
    )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")


    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)




class Profile(db.Model):
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


class Journal(db.Model):
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
        "Profile", backref=db.backref("journals", lazy=True)
    )  # noqa E501


class Plan(db.Model):
    __tablename__ = "plans"
    plan_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # noqa E501
    profile_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("profiles.profile_id")
    )  # noqa E501
    created_on = db.Column(DateTime, default=func.now())
    profile = db.relationship(
        "Profile", backref=db.backref("plans", lazy=True)
    )  # noqa E501


class VectorEmbeddings(db.Model):
    __tablename__ = "vector_embeddings"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = db.Column(String, unique=True, nullable=False)
    text = db.Column(Text, nullable=False)
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())

    embedding = db.Column(Vector(384), nullable=True)
    profile_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("profiles.user_id")

    )  # noqa E501
