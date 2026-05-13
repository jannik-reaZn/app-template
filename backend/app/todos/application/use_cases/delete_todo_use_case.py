from __future__ import annotations

from app.core import DomainError, Result
from app.todos.application.commands.delete_todo_command import DeleteTodoCommand
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort


class DeleteTodoUseCase:
    def __init__(self, todo_repository: TodoRepositoryPort) -> None:
        self.todo_repository = todo_repository

    def __call__(self, command: DeleteTodoCommand) -> Result[None, DomainError]:
        return self.todo_repository.delete(command.todo_id)
