from __future__ import annotations

from typing import Protocol

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import Todo


class TodoRepository(Protocol):
    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]: ...

    def save(self, todo: Todo) -> Result[Todo, DomainError]: ...
