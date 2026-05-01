from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import Todo, TodoStatus
from app.todos.domain.interfaces.todo_repository import TodoRepository


class CreateTodoUseCase:
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    def __call__(
        self, title: str, status: TodoStatus = TodoStatus.PENDING
    ) -> Result[Todo, DomainError]:
        todo_result = Todo.create(title=title, status=status)
        if todo_result.is_err:
            return todo_result
        return self.todo_repository.save(todo_result.value)
