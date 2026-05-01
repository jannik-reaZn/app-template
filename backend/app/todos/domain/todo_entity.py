from __future__ import annotations

from typing import Literal
from uuid import uuid4

from pydantic import Field

from app.core import DomainError, DomainModel, Result
from app.todos.domain.todo_errors import EmptyTodoTitleError

TodoStatus = Literal["pending", "completed"]


class Todo(DomainModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    title: str = Field(examples=["Pay electricity bill"])
    status: TodoStatus = Field(examples=["pending", "completed"])

    @classmethod
    def create(cls, title: str) -> Result[Todo, DomainError]:
        normalized_title: str = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(title=normalized_title, status="pending"))
