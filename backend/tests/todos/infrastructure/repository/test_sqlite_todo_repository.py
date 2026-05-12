import pytest
from sqlalchemy import select

from app.infrastructure.database.sqlite import SqliteSession
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.infrastructure.database.todo_model import TodoRecord
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from tests.factory.todo_factory import TodoFactory


class TestSqliteTodoRepository:
    @pytest.fixture(autouse=True)
    def setup(self, sqlite_session: SqliteSession) -> None:
        self.session = sqlite_session.session
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

        record = self.session.scalar(
            select(TodoRecord).where(TodoRecord.todo_id == todo.id)
        )

        assert record is not None
        assert record.id is not None
        assert record.todo_id == todo.id
        assert record.created_at is not None
        assert record.updated_at is not None
        assert record.updated_by == "Sytem"

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

    def test_save_updates_existing_row_for_same_domain_id(self) -> None:
        # GIVEN
        todo = TodoFactory.build()
        updated_todo = todo.model_copy(
            update={
                "title": todo.title.model_copy(update={"value": "Updated title"}),
            }
        )

        # WHEN
        first_result = self.repository.save(todo)
        second_result = self.repository.save(updated_todo)
        records = self.session.scalars(
            select(TodoRecord).where(TodoRecord.todo_id == todo.id)
        ).all()

        # THEN
        assert first_result.is_ok is True
        assert second_result.is_ok is True
        assert len(records) == 1
        assert records[0].title == "Updated title"
