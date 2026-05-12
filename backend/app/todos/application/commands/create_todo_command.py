from __future__ import annotations

from dataclasses import dataclass

from app.todos.domain.enums.todo_status import TodoStatus


@dataclass(frozen=True, slots=True)
class CreateTodoCommand:
    title: str
    status: TodoStatus = TodoStatus.PENDING
