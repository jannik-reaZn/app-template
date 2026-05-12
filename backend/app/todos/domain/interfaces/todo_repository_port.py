from __future__ import annotations

from typing import Protocol

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import TodoEntity


class TodoRepositoryPort(Protocol):
    def get_by_id(self, todo_id: str) -> Result[TodoEntity, DomainError]: ...

    def save(self, todo: TodoEntity) -> Result[TodoEntity, DomainError]: ...
