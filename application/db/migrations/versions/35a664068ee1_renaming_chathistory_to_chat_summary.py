"""Renaming ChatHistory to chat_summary

Revision ID: 35a664068ee1
Revises: 452f717e13e8
Create Date: 2025-03-11 16:15:53.649271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "35a664068ee1"
down_revision = "452f717e13e8"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
