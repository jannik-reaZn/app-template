from __future__ import annotations

from typing import Protocol

from app.core import Result

from app.domain.todos.entities import Todo
from app.domain.todos.errors import DomainError


class TodoRepository(Protocol):
    def save(self, todo: Todo) -> Result[Todo, DomainError]: ...
