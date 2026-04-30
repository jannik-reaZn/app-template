from __future__ import annotations

from app.core import DomainError


class EmptyTodoTitleError(DomainError):
    def __init__(self) -> None:
        super().__init__("Todo title cannot be empty")
