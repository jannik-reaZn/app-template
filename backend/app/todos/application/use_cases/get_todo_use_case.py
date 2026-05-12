from __future__ import annotations

from app.core import DomainError, Result
from app.todos.application.queries.get_todo_query import GetTodoQuery
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort


class GetTodoUseCase:
    def __init__(self, todo_repository: TodoRepositoryPort) -> None:
        self.todo_repository = todo_repository

    def __call__(self, query: GetTodoQuery) -> Result[TodoEntity, DomainError]:
        return self.todo_repository.get_by_id(query.todo_id)
