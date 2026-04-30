from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.core import Result

from app.todos.domain.errors import EmptyTodoTitleError

TodoStatus = Literal["pending", "completed"]


@dataclass(frozen=True, slots=True)
class Todo:
    id: str
    title: str
    status: TodoStatus

    @classmethod
    def create(cls, todo_id: str, title: str) -> Result["Todo", EmptyTodoTitleError]:
        normalized_title = title.strip()
        if not normalized_title:
            return Result.err(EmptyTodoTitleError())
        return Result.ok(cls(id=todo_id, title=normalized_title, status="pending"))
