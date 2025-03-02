"""Fix embeddings table to use user_id

Revision ID: 5240098bce48
Revises: 57e98a80c677
Create Date: 2025-03-02 19:35:44.184561

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "5240098bce48"
down_revision = "57e98a80c677"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vector_embeddings", schema=None) as batch_op:
        batch_op.drop_constraint(
            "vector_embeddings_profile_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(None, "profiles", ["profile_id"], ["user_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vector_embeddings", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "vector_embeddings_profile_id_fkey",
            "profiles",
            ["profile_id"],
            ["profile_id"],
        )

    # ### end Alembic commands ###
