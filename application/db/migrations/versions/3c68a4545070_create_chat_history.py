"""create chat history

Revision ID: 3c68a4545070
Revises: 6960772d9f80
Create Date: 2025-03-10 17:56:57.538864

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "3c68a4545070"
down_revision = "6960772d9f80"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
