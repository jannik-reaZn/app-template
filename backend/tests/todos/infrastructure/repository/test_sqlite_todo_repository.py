import pytest
from sqlalchemy import select

from app.infrastructure.database.sqlite import SqliteSession
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.value_objects.todo_note import TodoNote
from app.todos.domain.value_objects.todo_tag import TodoTag
from app.todos.infrastructure.database.todo_model import (
    TodoNoteRecord,
    TodoRecord,
    TodoTagLinkRecord,
    TodoTagRecord,
)
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

    def test_save_persists_todo_notes(self) -> None:
        # GIVEN
        todo = TodoFactory.build(
            notes=(
                TodoNote(content="Buy oat milk"),
                TodoNote(content="Check pantry first"),
            )
        )

        # WHEN
        result = self.repository.save(todo)
        persisted_todo = self.repository.get_by_id(todo.id)
        note_records = self.session.scalars(
            select(TodoNoteRecord).where(TodoNoteRecord.todo_id == todo.id)
        ).all()

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_ok is True
        assert persisted_todo.value.notes == todo.notes
        assert [record.content for record in note_records] == [
            "Buy oat milk",
            "Check pantry first",
        ]

    def test_save_persists_non_existing_tags(self) -> None:
        # GIVEN
        tags: list[str] = ["errands", "groceries"]
        todo = TodoFactory.build(tags=tuple(TodoTag(name=tag) for tag in tags))

        # WHEN
        persisted_todo = self.repository.save(todo)
        tag_records = self.session.scalars(select(TodoTagRecord)).all()
        tag_links = self.session.scalars(
            select(TodoTagLinkRecord).where(TodoTagLinkRecord.todo_id == todo.id)
        ).all()

        # THEN
        assert persisted_todo.is_ok is True
        assert persisted_todo.value.tags == todo.tags
        assert sorted(record.name for record in tag_records) == sorted(tags)
        assert sorted(link.tag_name for link in tag_links) == sorted(tags)

    def test_save_reuses_existing_tags(self) -> None:
        # GIVEN
        first_todo = TodoFactory.build(
            tags=(
                TodoTag(name="groceries"),
                TodoTag(name="weekly"),
            )
        )
        second_todo = TodoFactory.build(
            tags=(
                TodoTag(name="groceries"),
                TodoTag(name="urgent"),
            )
        )

        # WHEN
        first_result = self.repository.save(first_todo)
        second_result = self.repository.save(second_todo)

        tag_records = self.session.scalars(select(TodoTagRecord)).all()
        groceries_records = self.session.scalars(
            select(TodoTagRecord).where(TodoTagRecord.name == "groceries")
        ).all()
        groceries_links = self.session.scalars(
            select(TodoTagLinkRecord).where(TodoTagLinkRecord.tag_name == "groceries")
        ).all()

        # THEN
        assert first_result.is_ok is True
        assert second_result.is_ok is True
        # The "groceries" tag should only be created once and linked to both todos
        assert sorted(record.name for record in tag_records) == [
            "groceries",
            "urgent",
            "weekly",
        ]
        assert len(groceries_records) == 1
        assert sorted(link.todo_id for link in groceries_links) == sorted(
            [first_todo.id, second_todo.id]
        )
