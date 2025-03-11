"""Renaming table to chat_summary and adding summary column

Revision ID: af079374b327
Revises: 35a664068ee1
Create Date: 2025-03-11 16:21:51.276889

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "af079374b327"
down_revision = "35a664068ee1"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
