from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base_model import Base
from app.todos.domain.entities.todo_entity import Todo, TodoStatus


class TodoRecord(Base):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    def from_domain(cls, todo: Todo) -> TodoRecord:
        return cls(id=todo.id, title=todo.title, status=todo.status)

    def to_domain(self) -> Todo:
        return Todo(
            id=self.id,
            title=self.title,
            status=TodoStatus(self.status),
        )
