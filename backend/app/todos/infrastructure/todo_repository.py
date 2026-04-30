from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities import Todo


class InMemoryTodoRepository:
    def __init__(self) -> None:
        self.items: dict[str, Todo] = {}

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.items[todo.id] = todo
        return Result.ok(todo)