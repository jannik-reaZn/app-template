import pytest

from app.infrastructure.database.sqlite import SqliteSession
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.delete_todo_use_case import DeleteTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.infrastructure.repository.in_memory_todo_repository import (
    InMemoryTodoRepository,
)
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)


@pytest.fixture
def todo_in_memory_repository() -> InMemoryTodoRepository:
    return InMemoryTodoRepository()


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


@pytest.fixture
def delete_todo_use_case(
    todo_repository: SqliteTodoRepository,
) -> DeleteTodoUseCase:
    return DeleteTodoUseCase(todo_repository)
