"""add task avatar url

Revision ID: 0005_add_task_avatar_url
Revises: 0004_create_comments_table
Create Date: 2026-03-30 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_add_task_avatar_url"
down_revision = "0004_create_comments_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("avatar_url", sa.String(length=1024), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "avatar_url")
