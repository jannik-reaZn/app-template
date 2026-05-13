from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base_model import Base


class TodoRecord(Base):
    __tablename__ = "todos"

    todo_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[list[TodoNoteRecord]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan",
        order_by="TodoNoteRecord.position",
    )
    tag_links: Mapped[list[TodoTagLinkRecord]] = relationship(
        back_populates="todo",
        cascade="all, delete-orphan",
        order_by="TodoTagLinkRecord.tag_name",
    )


class TodoNoteRecord(Base):
    __tablename__ = "todo_notes"

    todo_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("todos.todo_id"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    todo: Mapped[TodoRecord] = relationship(back_populates="notes")


class TodoTagRecord(Base):
    __tablename__ = "todo_tags"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    todo_links: Mapped[list[TodoTagLinkRecord]] = relationship(back_populates="tag")


class TodoTagLinkRecord(Base):
    __tablename__ = "todo_tag_links"
    __table_args__ = (UniqueConstraint("todo_id", "tag_name"),)

    todo_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("todos.todo_id"),
        nullable=False,
    )
    tag_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("todo_tags.name"),
        nullable=False,
    )

    todo: Mapped[TodoRecord] = relationship(back_populates="tag_links")
    tag: Mapped[TodoTagRecord] = relationship(back_populates="todo_links")
