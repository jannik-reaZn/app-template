import pytest

from app.core import Result
from app.todos.domain.entities.todo_entity import Todo
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.presentation.responses.todo_response import TodoResponse
from app.todos.presentation.todo_presenter import TodoPresenter
from tests.factory.todo_factory import TodoFactory


class TestTodoPresenter:
    @pytest.fixture(autouse=True)
    def setup(self, todo_factory: TodoFactory) -> None:
        self.presenter = TodoPresenter()
        self.todo: Todo = todo_factory.build()

    def test_returns_todo_response_for_ok_result(self) -> None:
        response = self.presenter.present(Result.ok(self.todo))

        assert response == TodoResponse(
            id=self.todo.id,
            title=self.todo.title.value,
            status=self.todo.status,
        )

    def test_raises_domain_error_for_err_result(self) -> None:
        error = TodoNotFoundError("missing-todo")

        with pytest.raises(TodoNotFoundError, match="Todo not found"):
            self.presenter.present(Result.err(error))
