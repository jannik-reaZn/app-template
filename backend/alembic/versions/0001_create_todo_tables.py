"""create todo tables

Revision ID: 0001_create_todo_tables
Revises: None
Create Date: 2026-05-13 00:00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001_create_todo_tables"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "todos",
        sa.Column("todo_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("todo_id"),
    )
    op.create_table(
        "todo_tags",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "todo_notes",
        sa.Column("todo_id", sa.String(length=255), nullable=False),
        sa.Column("content", sa.String(length=255), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["todo_id"], ["todos.todo_id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "todo_tag_links",
        sa.Column("todo_id", sa.String(length=255), nullable=False),
        sa.Column("tag_name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_by", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["tag_name"], ["todo_tags.name"]),
        sa.ForeignKeyConstraint(["todo_id"], ["todos.todo_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("todo_id", "tag_name"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("todo_tag_links")
    op.drop_table("todo_notes")
    op.drop_table("todo_tags")
    op.drop_table("todos")
