from uuid import UUID

import pytest

from app.core import DomainError, Result
from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.domain.todo_entity import Todo, TodoStatus
from app.todos.domain.todo_errors import EmptyTodoTitleError


class TestCreateTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(self, create_todo_use_case: CreateTodoUseCase) -> None:
        self.create_todo_use_case = create_todo_use_case

    def test_returns_pending_todo(self) -> None:
        # GIVEN
        title: str = "Pay electricity bill"
        pending: TodoStatus = TodoStatus.PENDING

        # WHEN
        todo: Result[Todo, DomainError] = self.create_todo_use_case(
            title=title, status=pending
        )

        # THEN
        assert todo.is_ok is True
        assert UUID(todo.value.id)
        assert todo.value.title == title
        assert todo.value.status == "pending"

    def test_returns_error_for_blank_title(self) -> None:
        # GIVEN
        title: str = "   "

        # WHEN
        todo: Result[Todo, DomainError] = self.create_todo_use_case(title=title)

        # THEN
        assert todo.is_err is True
        assert isinstance(todo.error, EmptyTodoTitleError)
