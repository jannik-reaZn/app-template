import pytest

from app.infrastructure.database.sqlite import SqliteSession
from app.todos.infrastructure.repository.in_memory_todo_repository import (
    InMemoryTodoRepository,
)
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from app.todos.infrastructure.repository.todo_repository_backend import (
    TodoRepositoryType,
)
from app.todos.presentation.dependencies import todo_dependencies


class TestTodoDependencies:
    @pytest.fixture(autouse=True)
    def clear_dependency_caches(self) -> None:
        todo_dependencies.get_sqlite_session.cache_clear()
        todo_dependencies.get_in_memory_todo_repository.cache_clear()

    def test_get_todo_repository_uses_sqlite_backend(
        self,
        monkeypatch: pytest.MonkeyPatch,
        sqlite_session: SqliteSession,
    ) -> None:
        monkeypatch.setattr(
            todo_dependencies.settings.todo,
            "repository_backend",
            TodoRepositoryType.SQLITE,
        )
        monkeypatch.setattr(
            todo_dependencies,
            "get_sqlite_session",
            lambda: sqlite_session,
        )

        repository = todo_dependencies.get_todo_repository()

        assert isinstance(repository, SqliteTodoRepository)

    def test_get_todo_repository_uses_in_memory_backend(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            todo_dependencies.settings.todo,
            "repository_backend",
            TodoRepositoryType.IN_MEMORY,
        )

        repository = todo_dependencies.get_todo_repository()

        assert isinstance(repository, InMemoryTodoRepository)
