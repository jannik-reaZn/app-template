from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.todo_entity import Todo
from app.todos.domain.todo_repository import TodoRepository


class CreateTodoUseCase:
    def __init__(self, todo_repository: TodoRepository) -> None:
        self.todo_repository = todo_repository

    def execute(self, title: str) -> Result[Todo, DomainError]:
        todo_result = Todo.create(title=title)
        if todo_result.is_err:
            return todo_result
        return self.todo_repository.save(todo_result.value)
