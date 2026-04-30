from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic.fields import Field

from app.core import DomainError, Result
from app.todos.domain.errors import EmptyTodoTitleError

TodoStatus = Literal["pending", "completed"]


@dataclass(frozen=True, slots=True)
class Todo:
    id: str = Field(examples=["todo-123"])
    title: str = Field(examples=["Pay electricity bill"])
    status: TodoStatus = Field(examples=["pending", "completed"])

    @classmethod
    def create(cls, todo_id: str, title: str) -> Result[Todo, DomainError]:
        normalized_title: str = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(id=todo_id, title=normalized_title, status="pending"))
