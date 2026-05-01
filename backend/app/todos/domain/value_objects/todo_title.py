from __future__ import annotations

from pydantic import Field

from app.core import DomainError, DomainModel, Result
from app.todos.domain.errors.todo_errors import EmptyTodoTitleError


class TodoTitle(DomainModel):
    value: str = Field(
        title="Todo title",
        description="A normalized, non-empty title for a todo item.",
        examples=["Pay electricity bill"],
    )

    @classmethod
    def create(cls, raw: str) -> Result[TodoTitle, DomainError]:
        normalized_value = raw.strip()
        if not normalized_value:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(value=normalized_value))

    def __str__(self) -> str:
        return self.value
