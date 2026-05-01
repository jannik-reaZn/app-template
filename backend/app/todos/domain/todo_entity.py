from __future__ import annotations

from enum import StrEnum, auto
from uuid import uuid4

from pydantic import Field

from app.core import DomainError, DomainModel, Result
from app.todos.domain.todo_errors import EmptyTodoTitleError


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
    title: str = Field(
        title="Title of the todo item",
        description="A brief description of the task to be completed.",
        examples=["Pay electricity bill"],
    )
    status: TodoStatus = Field(
        title="Status of the todo item",
        description="The current status of the todo item, either pending or completed.",
        default=TodoStatus.PENDING,
        examples=["pending", "completed"],
    )

    @classmethod
    def create(cls, title: str) -> Result[Todo, DomainError]:
        normalized_title: str = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(title=normalized_title))
