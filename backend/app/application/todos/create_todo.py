from __future__ import annotations

from typing import Protocol

from app.core import Result
from app.domain.todos.entities import Todo
from app.domain.todos.errors import DomainError
from app.domain.todos.repositories import TodoRepository


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
