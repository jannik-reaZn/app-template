from __future__ import annotations

from typing import Protocol

from app.core import DomainError, Result
from app.todos.domain.todo_entity import Todo
from app.todos.domain.todo_repository import TodoRepository


class TodoIdGenerator(Protocol):
    def new(self) -> str: ...


class CreateTodoUseCase:
    def __init__(
        self, todo_repository: TodoRepository, id_generator: TodoIdGenerator
    ) -> None:
        self.todo_repository = todo_repository
        self.id_generator = id_generator

    def execute(self, title: str) -> Result[Todo, DomainError]:
        todo_result = Todo.create(todo_id=self.id_generator.new(), title=title)
        if todo_result.is_err:
            return todo_result
        return self.todo_repository.save(todo_result.value)
