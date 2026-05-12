from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.enums.todo_status import TodoStatus
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort


class CreateTodoUseCase:
    def __init__(self, todo_repository: TodoRepositoryPort) -> None:
        self.todo_repository = todo_repository

    def __call__(
        self, title: str, status: TodoStatus = TodoStatus.PENDING
    ) -> Result[TodoEntity, DomainError]:
        todo_result = TodoEntity.create(title=title, status=status)
        if todo_result.is_err:
            return todo_result
        return self.todo_repository.save(todo_result.value)
