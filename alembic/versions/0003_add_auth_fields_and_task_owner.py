"""add task owner

Revision ID: 0003_auth_task_owner
Revises: 0002_create_tasks_table
Create Date: 2026-03-21 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_auth_task_owner"
down_revision = "0002_create_tasks_table"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("owner_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_tasks_owner_id"), "tasks", ["owner_id"], unique=False)
    op.create_foreign_key("fk_tasks_owner_id_users", "tasks", "users", ["owner_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_tasks_owner_id_users", "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_owner_id"), table_name="tasks")
    op.drop_column("tasks", "owner_id")
