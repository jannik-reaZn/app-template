from __future__ import annotations

from itertools import count

from app.core import Result
from app.todos.domain.entities import Todo
from app.todos.domain.errors import DomainError


class InMemoryTodoRepository:
    def __init__(self) -> None:
        self.items: dict[str, Todo] = {}

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.items[todo.id] = todo
        return Result.ok(todo)


class SequentialTodoIdGenerator:
    def __init__(self) -> None:
        self._sequence = count(1)

    def new(self) -> str:
        return f"todo-{next(self._sequence)}"
