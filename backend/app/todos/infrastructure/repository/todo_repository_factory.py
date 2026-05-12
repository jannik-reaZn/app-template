from __future__ import annotations

from typing import assert_never

from app.infrastructure.database.sqlite import SqliteSession
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.repository.in_memory_todo_repository import (
    InMemoryTodoRepository,
)
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from app.todos.infrastructure.repository.todo_repository_backend import (
    TodoRepositoryType,
)


def create_todo_repository(
    backend: TodoRepositoryType,
    *,
    sqlite_session: SqliteSession,
    in_memory_repository: InMemoryTodoRepository,
) -> TodoRepositoryPort:
    match backend:
        case TodoRepositoryType.IN_MEMORY:
            return in_memory_repository
        case TodoRepositoryType.SQLITE:
            return SqliteTodoRepository(sqlite_session)
        case _:
            assert_never(backend)
