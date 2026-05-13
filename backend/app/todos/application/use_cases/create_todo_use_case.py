from __future__ import annotations

from app.core import DomainError, Result
from app.todos.application.commands.create_todo_command import CreateTodoCommand
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.domain.value_objects.todo_note import TodoNote


class CreateTodoUseCase:
    def __init__(self, todo_repository: TodoRepositoryPort) -> None:
        self.todo_repository = todo_repository

    def __call__(self, command: CreateTodoCommand) -> Result[TodoEntity, DomainError]:
        todo_result = TodoEntity.create(
            title=command.title,
            status=command.status,
            notes=tuple(TodoNote(content=note) for note in command.notes),
        )
        if todo_result.is_err:
            return todo_result
        return self.todo_repository.save(todo_result.value)
