"""replace chat history with chat summary

Revision ID: fffda80e3f2d
Revises: 9ab9334420ed
Create Date: 2025-03-11 14:46:28.018524

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "fffda80e3f2d"
down_revision = "9ab9334420ed"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "chat_summary",
        sa.Column("chat_id", sa.UUID(), primary_key=True),
        sa.Column(
            "profile_id", sa.UUID(), sa.ForeignKey("profiles.profile_id")
        ),
        sa.Column("summary", sa.Text()),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("chat_summary")
