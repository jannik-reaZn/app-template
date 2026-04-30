from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities import Todo
from app.todos.domain.repositories import TodoRepository


class GetTodoUseCase:
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    def execute(self, todo_id: str) -> Result[Todo, DomainError]:
        return self.todo_repository.get_by_id(todo_id)
