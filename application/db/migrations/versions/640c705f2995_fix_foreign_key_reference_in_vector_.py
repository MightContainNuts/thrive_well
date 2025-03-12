"""Fix foreign key reference in vector_embeddings

Revision ID: 640c705f2995
Revises:
Create Date: 2025-03-03 10:38:46.542223

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "640c705f2995"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vector_embeddings", schema=None) as batch_op:
        batch_op.drop_index(
            "vector_embeddings_embedding_idx",
            postgresql_with={"lists": "100"},
            postgresql_using="ivfflat",
        )
        batch_op.drop_constraint(
            "vector_embeddings_profile_id_fkey", type_="foreignkey"
        )
        batch_op.create_foreign_key(None, "profiles", ["profile_id"], ["profile_id"])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("vector_embeddings", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.create_foreign_key(
            "vector_embeddings_profile_id_fkey", "profiles", ["profile_id"], ["user_id"]
        )
        batch_op.create_index(
            "vector_embeddings_embedding_idx",
            ["embedding"],
            unique=False,
            postgresql_with={"lists": "100"},
            postgresql_using="ivfflat",
        )

    # ### end Alembic commands ###
