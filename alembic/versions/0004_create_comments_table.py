"""create comments table

Revision ID: 0004_create_comments_table
Revises: 0003_auth_task_owner
Create Date: 2026-03-28 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_create_comments_table"
down_revision = "0003_auth_task_owner"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], name="fk_comments_task_id_tasks"),
    )
    op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
    op.create_index(op.f("ix_comments_task_id"), "comments", ["task_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_comments_task_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_id"), table_name="comments")
    op.drop_table("comments")
