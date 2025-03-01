"""fix User to include hashed password

Revision ID: e18dfcb0e3dc
Revises: 2b68240d181b
Create Date: 2025-02-27 11:18:26.746587

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e18dfcb0e3dc"
down_revision = "2b68240d181b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_name", sa.String(length=64), nullable=True))
        batch_op.add_column(
            sa.Column("password_hash", sa.String(length=128), nullable=True)
        )
        batch_op.add_column(sa.Column("created_on", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("updated_on", sa.DateTime(), nullable=True))
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(length=120),
            type_=sa.String(length=100),
            nullable=True,
        )
        batch_op.drop_constraint("users_google_id_key", type_="unique")
        batch_op.create_unique_constraint(None, ["user_name"])
        batch_op.drop_column("name")
        batch_op.drop_column("locale")
        batch_op.drop_column("family_name")
        batch_op.drop_column("picture")
        batch_op.drop_column("given_name")
        batch_op.drop_column("google_id")
        batch_op.drop_column("created_at")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "google_id", sa.VARCHAR(length=255), autoincrement=False, nullable=False
            )
        )
        batch_op.add_column(
            sa.Column(
                "given_name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "picture", sa.VARCHAR(length=255), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "family_name",
                sa.VARCHAR(length=255),
                autoincrement=False,
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "locale", sa.VARCHAR(length=50), autoincrement=False, nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "name", sa.VARCHAR(length=255), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_constraint(None, type_="unique")
        batch_op.create_unique_constraint("users_google_id_key", ["google_id"])
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=120),
            nullable=False,
        )
        batch_op.drop_column("updated_on")
        batch_op.drop_column("created_on")
        batch_op.drop_column("password_hash")
        batch_op.drop_column("user_name")

    # ### end Alembic commands ###
