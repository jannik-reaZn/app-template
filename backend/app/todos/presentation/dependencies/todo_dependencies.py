from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.infrastructure.database.base_model import Base
from app.infrastructure.database.sqlite import SqliteSession
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.repository.in_memory_todo_repository import (
    InMemoryTodoRepository,
)
from app.todos.infrastructure.repository.todo_repository_factory import (
    create_todo_repository,
)
from app.todos.presentation.todo_presenter import TodoPresenter
from settings import settings


@lru_cache
def get_sqlite_session() -> SqliteSession:
    return SqliteSession(
        metadata=Base.metadata,
        database_path=settings.database.todo_db_path,
    )


@lru_cache
def get_in_memory_todo_repository() -> InMemoryTodoRepository:
    return InMemoryTodoRepository()


def get_todo_repository() -> TodoRepositoryPort:
    return create_todo_repository(
        settings.todo.repository_backend,
        sqlite_session=get_sqlite_session(),
        in_memory_repository=get_in_memory_todo_repository(),
    )


def get_create_todo_use_case(
    todo_repository: Annotated[TodoRepositoryPort, Depends(get_todo_repository)],
) -> CreateTodoUseCase:
    return CreateTodoUseCase(todo_repository)


def get_get_todo_use_case(
    todo_repository: Annotated[TodoRepositoryPort, Depends(get_todo_repository)],
) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)


def get_todo_presenter() -> TodoPresenter:
    return TodoPresenter()
