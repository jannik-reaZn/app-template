from __future__ import annotations

from enum import StrEnum, auto
from uuid import uuid4

from pydantic import Field

from app.core import DomainError, DomainModel, Result
from app.todos.domain.errors.todo_errors import EmptyTodoTitleError
from app.todos.domain.value_objects.todo_title import TodoTitle


class TodoStatus(StrEnum):
    PENDING = auto()
    COMPLETED = auto()


class Todo(DomainModel):
    id: str = Field(
        title="Todo ID",
        description="A UUID string that uniquely identifies the todo item.",
        default_factory=lambda: str(uuid4()),
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    title: TodoTitle = Field(title="Title of the todo item")
    status: TodoStatus = Field(
        title="Status of the todo item",
        description="The current status of the todo item, either pending or completed.",
        default=TodoStatus.PENDING,
        examples=["pending", "completed"],
    )

    @classmethod
    def create(
        cls, title: str, status: TodoStatus = TodoStatus.PENDING
    ) -> Result[Todo, DomainError]:
        title_result = TodoTitle.create(title)
        if title_result.is_err:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(title=title_result.value, status=status))
