from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.database.base_model import Base
from app.core.database.sqlite import SqliteSession
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.domain.todo_repository import TodoRepository
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from settings import settings


@lru_cache
def get_sqlite_session() -> SqliteSession:
    return SqliteSession(
        metadata=Base.metadata,
        database_path=settings.database.todo_db_path,
    )


def get_todo_repository(
    session: Annotated[SqliteSession, Depends(get_sqlite_session)],
) -> TodoRepository:
    return SqliteTodoRepository(session)


def get_create_todo_use_case(
    todo_repository: Annotated[TodoRepository, Depends(get_todo_repository)],
) -> CreateTodoUseCase:
    return CreateTodoUseCase(todo_repository)


def get_get_todo_use_case(
    todo_repository: Annotated[TodoRepository, Depends(get_todo_repository)],
) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)
