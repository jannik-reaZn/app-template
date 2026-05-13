from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort


class InMemoryTodoRepository(TodoRepositoryPort):
    def __init__(self) -> None:
        self.items: dict[str, TodoEntity] = {}

    def get_by_id(self, todo_id: str) -> Result[TodoEntity, DomainError]:
        todo = self.items.get(todo_id)
        if todo is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(todo)

    def save(self, todo: TodoEntity) -> Result[TodoEntity, DomainError]:
        self.items[todo.id] = todo
        return Result.ok(todo)

    def delete(self, todo_id: str) -> Result[None, DomainError]:
        if todo_id not in self.items:
            return Result.err(TodoNotFoundError(todo_id))

        del self.items[todo_id]
        return Result.ok(None)
