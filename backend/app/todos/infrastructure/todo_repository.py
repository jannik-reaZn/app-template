from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities import Todo
from app.todos.domain.todo_errors import TodoNotFoundError


class InMemoryTodoRepository:
    def __init__(self) -> None:
        self.items: dict[str, Todo] = {}

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        todo = self.items.get(todo_id)
        if todo is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(todo)

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.items[todo.id] = todo
        return Result.ok(todo)
