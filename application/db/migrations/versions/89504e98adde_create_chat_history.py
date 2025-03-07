"""create chat history

Revision ID: 89504e98adde
Revises: d1b980b6f289
Create Date: 2025-03-07 16:54:57.278857

"""
from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision = "89504e98adde"
down_revision = "d1b980b6f289"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("chat_history", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_query", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_response", sa.Text(), nullable=True))
        batch_op.drop_column("response")
        batch_op.drop_column("query")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("chat_history", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("query", sa.TEXT(), autoincrement=False, nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "response", sa.TEXT(), autoincrement=False, nullable=True
            )
        )
        batch_op.drop_column("ai_response")
        batch_op.drop_column("user_query")

    # ### end Alembic commands ###
