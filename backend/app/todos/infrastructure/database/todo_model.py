from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
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
