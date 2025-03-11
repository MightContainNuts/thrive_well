"""create chat history

Revision ID: 6960772d9f80
Revises: d2744f719c94
Create Date: 2025-03-10 17:56:13.432278

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "6960772d9f80"
down_revision = "d2744f719c94"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
