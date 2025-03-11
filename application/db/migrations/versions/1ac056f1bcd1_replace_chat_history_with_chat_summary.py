"""replace chat history with chat summary

Revision ID: 1ac056f1bcd1
Revises: fffda80e3f2d
Create Date: 2025-03-11 15:34:13.845046

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "1ac056f1bcd1"
down_revision = "fffda80e3f2d"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
