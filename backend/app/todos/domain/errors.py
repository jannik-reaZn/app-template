from __future__ import annotations


class DomainError(Exception):
    pass


class EmptyTodoTitleError(DomainError):
    def __init__(self) -> None:
        super().__init__("Todo title cannot be empty")
