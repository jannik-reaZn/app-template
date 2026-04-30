from __future__ import annotations

from typing import Protocol

from app.core import Result

from app.todos.domain.entities import Todo
from app.todos.domain.errors import DomainError


class TodoRepository(Protocol):
    def save(self, todo: Todo) -> Result[Todo, DomainError]: ...
