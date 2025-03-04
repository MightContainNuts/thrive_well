from enum import Enum as PyEnum
import uuid


from sqlalchemy import Enum as SQLEnum, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from pgvector.sqlalchemy import Vector


from application.db_init import db


class RoleStatus(str, PyEnum):
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
    cancer_type = db.Column(String(100))
    medication = db.Column(String(100))
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), unique=True
    )  # noqa E501


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
    entry = db.Column(Text)
    created_on = db.Column(DateTime, default=func.now())
    ai_response = db.Column(JSON)
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
        UUID(as_uuid=True), db.ForeignKey("profiles.profile_id")
    )  # noqa E501


class Medications(db.Model):
    __tablename__ = "medications"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(String(100), unique=True)
    fda_code = db.Column(String(10), unique=True)
    description = db.Column(String(255))
    side_effects = db.Column(Vector(384), nullable=True)
    created_on = db.Column(DateTime, default=func.now())
    updated_on = db.Column(DateTime, default=func.now())
