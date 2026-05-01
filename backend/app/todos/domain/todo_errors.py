from __future__ import annotations

from app.core import DomainError


class EmptyTodoTitleError(DomainError):
    def __init__(self) -> None:
        super().__init__("Todo title cannot be empty")


class TodoNotFoundError(DomainError):
    def __init__(self, todo_id: str) -> None:
        super().__init__("Todo not found")
        self.todo_id = todo_id
