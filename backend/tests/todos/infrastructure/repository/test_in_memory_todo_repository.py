import pytest

from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.infrastructure.repository.in_memory_todo_repository import (
    InMemoryTodoRepository,
)


class TestInMemoryTodoRepository:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.repository = InMemoryTodoRepository()

    def test_save_persists_todo(self) -> None:
        # GIVEN
        todo = TodoEntity.create(title="Pay electricity bill").value

        # WHEN
        result = self.repository.save(todo)
        persisted_todo = self.repository.get_by_id(todo.id)

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_ok is True
        assert persisted_todo.value == todo

    def test_get_by_id_returns_not_found_error_for_missing_todo(self) -> None:
        # WHEN
        result = self.repository.get_by_id("missing-todo")

        # THEN
        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
        assert result.error.todo_id == "missing-todo"

    def test_delete_removes_existing_todo(self) -> None:
        # GIVEN
        todo = TodoEntity.create(title="Pay electricity bill").value
        self.repository.save(todo)

        # WHEN
        result = self.repository.delete(todo.id)
        persisted_todo = self.repository.get_by_id(todo.id)

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_err is True
        assert isinstance(persisted_todo.error, TodoNotFoundError)

    def test_delete_returns_not_found_error_for_missing_todo(self) -> None:
        # WHEN
        result = self.repository.delete("missing-todo")

        # THEN
        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
