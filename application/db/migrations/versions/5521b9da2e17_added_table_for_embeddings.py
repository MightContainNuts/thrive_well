"""added table for embeddings

Revision ID: 5521b9da2e17
Revises: 22d62371994e
Create Date: 2025-03-02 18:15:21.715557

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5521b9da2e17"
down_revision = "22d62371994e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vector_embeddings",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("embedding", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("profile_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profiles.profile_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("url"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vector_embeddings")
    # ### end Alembic commands ###
