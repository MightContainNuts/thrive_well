"""Manual update for chat_summary

Revision ID: d63c9fd09210
Revises: af079374b327
Create Date: 2025-03-11 16:22:59.237410

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "d63c9fd09210"
down_revision = "af079374b327"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
