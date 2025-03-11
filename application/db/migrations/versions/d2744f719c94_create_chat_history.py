"""create chat history

Revision ID: d2744f719c94
Revises: 46f06825b37f
Create Date: 2025-03-10 17:31:01.321386

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "d2744f719c94"
down_revision = "46f06825b37f"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
