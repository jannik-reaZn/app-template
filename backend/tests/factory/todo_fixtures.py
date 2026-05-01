from collections.abc import Iterator

import pytest

from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.infrastructure.database import SqliteSession
from app.todos.infrastructure.repository import (
    InMemoryTodoRepository,
    SqliteTodoRepository,
)


@pytest.fixture
def todo_in_memory_repository() -> InMemoryTodoRepository:
    return InMemoryTodoRepository()


@pytest.fixture
def sqlite_session() -> Iterator[SqliteSession]:
    session = SqliteSession(":memory:")
    yield session
    session.close()


@pytest.fixture
def todo_repository(sqlite_session: SqliteSession) -> SqliteTodoRepository:
    return SqliteTodoRepository(sqlite_session)


@pytest.fixture
def create_todo_use_case(todo_repository: SqliteTodoRepository) -> CreateTodoUseCase:
    return CreateTodoUseCase(todo_repository)


@pytest.fixture
def get_todo_use_case(
    todo_repository: SqliteTodoRepository,
) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)
