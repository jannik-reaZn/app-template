from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base_model import Base
from app.todos.domain.entities.todo_entity import Todo
from app.todos.domain.enum.todo_status import TodoStatus
from app.todos.domain.value_objects.todo_title import TodoTitle


class TodoRecord(Base):
    __tablename__ = "todos"

    todo_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    def from_domain(cls, todo: Todo) -> TodoRecord:
        return cls(todo_id=todo.id, title=todo.title.value, status=todo.status)

    def to_domain(self) -> Todo:
        return Todo(
            id=self.todo_id,
            title=TodoTitle(value=self.title),
            status=TodoStatus(self.status),
        )
