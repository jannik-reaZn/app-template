from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import Todo
from app.todos.domain.interfaces.todo_repository import TodoRepositoryPort


class GetTodoUseCase:
    def __init__(self, todo_repository: TodoRepositoryPort) -> None:
        self.todo_repository = todo_repository

    def __call__(self, todo_id: str) -> Result[Todo, DomainError]:
        return self.todo_repository.get_by_id(todo_id)
