import pytest

from app.core.database.sqlite import SqliteSession
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.infrastructure.repository import SqliteTodoRepository
from tests.factory.todo_factory import TodoFactory


class TestSqliteTodoRepository:
    @pytest.fixture(autouse=True)
    def setup(self, sqlite_session: SqliteSession) -> None:
        self.repository = SqliteTodoRepository(sqlite_session)

    def test_save_persists_todo(self) -> None:
        # GIVEN
        todo = TodoFactory.build()

        # WHEN
        result = self.repository.save(todo)
        persisted_todo = self.repository.get_by_id(todo.id)

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_ok is True
        assert persisted_todo.value == todo

    def test_get_by_id_returns_not_found_error_for_missing_todo(
        self,
    ) -> None:
        # GIVEN
        id: str = "missing-todo"

        # WHEN
        result = self.repository.get_by_id(id)

        # THEN
        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
        assert result.error.todo_id == id
