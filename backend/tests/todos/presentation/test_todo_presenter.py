import pytest

from app.core import Result
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.value_objects.todo_note import TodoNote
from app.todos.domain.value_objects.todo_tag import TodoTag
from app.todos.presentation.responses.todo_response import TodoResponse
from app.todos.presentation.todo_presenter import TodoPresenter
from tests.factory.todo_factory import TodoFactory


class TestTodoPresenter:
    @pytest.fixture(autouse=True)
    def setup(self, todo_factory: TodoFactory) -> None:
        self.presenter = TodoPresenter()
        self.todo: TodoEntity = todo_factory.build()

    def test_returns_todo_response_for_ok_result(self) -> None:
        response = self.presenter.present(Result.ok(self.todo))

        assert response == TodoResponse(
            id=self.todo.id,
            title=self.todo.title.value,
            status=self.todo.status,
            notes=[],
            tags=[],
        )

    def test_returns_notes_in_todo_response(self) -> None:
        todo = self.todo.model_copy(
            update={
                "notes": (
                    TodoNote(content="Buy oat milk"),
                    TodoNote(content="Check pantry first"),
                )
            }
        )

        response = self.presenter.present(Result.ok(todo))

        assert response.notes == ["Buy oat milk", "Check pantry first"]

    def test_returns_tags_in_todo_response(self) -> None:
        todo = self.todo.model_copy(
            update={
                "tags": (TodoTag(name="groceries"), TodoTag(name="weekly")),
            }
        )

        response = self.presenter.present(Result.ok(todo))

        assert response.tags == ["groceries", "weekly"]

    def test_raises_domain_error_for_err_result(self) -> None:
        error = TodoNotFoundError("missing-todo")

        with pytest.raises(TodoNotFoundError, match="TodoEntity not found"):
            self.presenter.present(Result.err(error))
