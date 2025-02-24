"""Initial migration

Revision ID: e354afbf55c0
Revises:
Create Date: 2025-02-16 14:52:59.307265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e354afbf55c0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("user_name", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column(
            "role",
            sa.Enum("MODERATOR", "USER", "ADMIN", name="rolestatus"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("user_id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("user_name"),
    )
    op.create_table(
        "activities",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("activity_type", sa.String(length=100), nullable=True),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "mood_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "mood",
            sa.Enum(
                "VERY_POSITIVE",
                "SOMEWHAT_POSITIVE",
                "NEUTRAL",
                "SOMEWHAT_NEGATIVE",
                "VERY_NEGATIVE",
                name="moodstatus",
            ),
            nullable=True,
        ),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "profiles",
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("user_name", sa.String(length=64), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column(
            "mood",
            sa.Enum(
                "VERY_POSITIVE",
                "SOMEWHAT_POSITIVE",
                "NEUTRAL",
                "SOMEWHAT_NEGATIVE",
                "VERY_NEGATIVE",
                name="moodstatus",
            ),
            nullable=True,
        ),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
        ),
        sa.PrimaryKeyConstraint("profile_id"),
        sa.UniqueConstraint("user_id"),
        sa.UniqueConstraint("user_name"),
    )
    op.create_table(
        "journals",
        sa.Column("journal_id", sa.UUID(), nullable=False),
        sa.Column("profile_id", sa.UUID(), nullable=True),
        sa.Column(
            "sentiment",
            sa.Enum(
                "VERY_POSITIVE",
                "SOMEWHAT_POSITIVE",
                "NEUTRAL",
                "SOMEWHAT_NEGATIVE",
                "VERY_NEGATIVE",
                name="moodstatus",
            ),
            nullable=True,
        ),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.profile_id"],
        ),
        sa.PrimaryKeyConstraint("journal_id"),
    )
    op.create_table(
        "plans",
        sa.Column("plan_id", sa.UUID(), nullable=False),
        sa.Column("profile_id", sa.UUID(), nullable=True),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.profile_id"],
        ),
        sa.PrimaryKeyConstraint("plan_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plans")
    op.drop_table("journals")
    op.drop_table("profiles")
    op.drop_table("mood_history")
    op.drop_table("activities")
    op.drop_table("users")
    # ### end Alembic commands ###
