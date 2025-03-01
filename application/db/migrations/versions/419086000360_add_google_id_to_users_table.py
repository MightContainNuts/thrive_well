"""Add google_id to users table

Revision ID: 419086000360
Revises: e354afbf55c0
Create Date: 2025-02-26 19:46:18.517245

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "419086000360"
down_revision = "e354afbf55c0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("google_id", sa.String(length=255), nullable=False)
        )
        batch_op.add_column(sa.Column("name", sa.String(length=255), nullable=True))
        batch_op.add_column(
            sa.Column("given_name", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(
            sa.Column("family_name", sa.String(length=255), nullable=True)
        )
        batch_op.add_column(sa.Column("picture", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("locale", sa.String(length=50), nullable=True))
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(length=100),
            type_=sa.String(length=120),
            nullable=False,
        )
        batch_op.drop_constraint("users_user_name_key", type_="unique")
        batch_op.create_unique_constraint(None, ["google_id"])
        batch_op.drop_column("created_on")
        batch_op.drop_column("user_name")
        batch_op.drop_column("updated_on")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "updated_on", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "user_name", sa.VARCHAR(length=64), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "created_on", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_constraint(None, type_="unique")
        batch_op.create_unique_constraint("users_user_name_key", ["user_name"])
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=120),
            type_=sa.VARCHAR(length=100),
            nullable=True,
        )
        batch_op.drop_column("locale")
        batch_op.drop_column("picture")
        batch_op.drop_column("family_name")
        batch_op.drop_column("given_name")
        batch_op.drop_column("name")
        batch_op.drop_column("google_id")

    # ### end Alembic commands ###
