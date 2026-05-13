from uuid import UUID

import pytest

from app.core import DomainError, Result
from app.todos.application.commands.create_todo_command import CreateTodoCommand
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.enums.todo_status import TodoStatus
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
        self.todo: TodoEntity = todo_factory.build(status=TodoStatus.PENDING)

    def test_returns_pending_todo(self) -> None:
        # GIVEN
        title: str = self.todo.title.value
        pending: TodoStatus = self.todo.status
        command = CreateTodoCommand(title=title, status=pending)

        # WHEN
        todo: Result[TodoEntity, DomainError] = self.create_todo_use_case(command)

        # THEN
        assert todo.is_ok is True
        assert UUID(todo.value.id)
        assert todo.value.title.value == title
        assert todo.value.status == "pending"

    def test_returns_error_for_blank_title(self) -> None:
        # GIVEN
        title: str = "   "
        command = CreateTodoCommand(title=title)

        # WHEN
        todo: Result[TodoEntity, DomainError] = self.create_todo_use_case(command)

        # THEN
        assert todo.is_err is True
        assert isinstance(todo.error, EmptyTodoTitleError)

    def test_returns_todo_with_notes(self) -> None:
        # GIVEN
        command = CreateTodoCommand(
            title="Buy groceries",
            notes=("Buy oat milk", "Check pantry first"),
        )

        # WHEN
        todo: Result[TodoEntity, DomainError] = self.create_todo_use_case(command)

        # THEN
        assert todo.is_ok is True
        assert [note.content for note in todo.value.notes] == [
            "Buy oat milk",
            "Check pantry first",
        ]
