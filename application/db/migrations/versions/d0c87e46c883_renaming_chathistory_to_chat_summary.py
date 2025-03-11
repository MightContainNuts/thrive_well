"""Renaming ChatHistory to chat_summary

Revision ID: d0c87e46c883
Revises: 1ac056f1bcd1
Create Date: 2025-03-11 15:38:10.309498

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "d0c87e46c883"
down_revision = "1ac056f1bcd1"
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table("chat_history", "chat_summary")


def downgrade():
    op.rename_table("chat_summary", "chat_history")
