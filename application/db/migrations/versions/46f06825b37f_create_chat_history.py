"""create chat history

Revision ID: 46f06825b37f
Revises: a5468d256c59
Create Date: 2025-03-07 18:06:07.459085

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "46f06825b37f"
down_revision = "a5468d256c59"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
