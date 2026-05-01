from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.todos.application.create_todo_use_case import (
    CreateTodoUseCase,
    TodoIdGenerator,
)
from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.domain.todo_repository import TodoRepository
from app.todos.infrastructure.todo_id_generator import SequentialTodoIdGenerator
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository


@lru_cache
def get_todo_repository() -> TodoRepository:
    return InMemoryTodoRepository()


@lru_cache
def get_todo_id_generator() -> TodoIdGenerator:
    return SequentialTodoIdGenerator()


def get_create_todo_use_case(
    todo_repository: Annotated[TodoRepository, Depends(get_todo_repository)],
    todo_id_generator: Annotated[TodoIdGenerator, Depends(get_todo_id_generator)],
) -> CreateTodoUseCase:
    return CreateTodoUseCase(todo_repository, todo_id_generator)


def get_get_todo_use_case(
    todo_repository: Annotated[TodoRepository, Depends(get_todo_repository)],
) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)
