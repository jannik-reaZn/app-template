import pytest

from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.domain.todo_errors import EmptyTodoTitleError


class TestCreateTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, create_todo_use_case: CreateTodoUseCase) -> None:
        self.create_todo_use_case = create_todo_use_case

    def test_returns_pending_todo(self) -> None:
        result = self.create_todo_use_case.execute(title="Pay electricity bill")

        assert result.is_ok is True
        assert result.value.id == "todo-123"
        assert result.value.title == "Pay electricity bill"
        assert result.value.status == "pending"

    def test_returns_error_for_blank_title(self) -> None:
        result = self.create_todo_use_case.execute(title="   ")

        assert result.is_err is True
        assert isinstance(result.error, EmptyTodoTitleError)
