"""remove pgvector

Revision ID: b2b1097f7ec6
Revises: 3c68bf94ab6c
Create Date: 2025-03-13 11:02:33.319997

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = 'b2b1097f7ec6'
down_revision = '3c68bf94ab6c'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
