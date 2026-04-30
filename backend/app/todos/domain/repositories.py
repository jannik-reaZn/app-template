from __future__ import annotations

from typing import Protocol

from app.core import DomainError, Result

from app.todos.domain.entities import Todo


class TodoRepository(Protocol):
    def save(self, todo: Todo) -> Result[Todo, DomainError]: ...
