from uuid import UUID

import pytest

from app.core import DomainError, Result
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.domain.entities.todo_entity import Todo, TodoStatus
from app.todos.domain.errors.todo_errors import EmptyTodoTitleError
from tests.factory.todo_factory import TodoFactory


class TestCreateTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        create_todo_use_case: CreateTodoUseCase,
        todo_factory: TodoFactory,
    ) -> None:
        self.create_todo_use_case = create_todo_use_case
        self.todo: Todo = todo_factory.build(status=TodoStatus.PENDING)

    def test_returns_pending_todo(self) -> None:
        # GIVEN
        title: str = self.todo.title
        pending: TodoStatus = self.todo.status

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
