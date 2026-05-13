import pytest

from app.core import DomainError, Result
from app.todos.application.commands.delete_todo_command import DeleteTodoCommand
from app.todos.application.use_cases.delete_todo_use_case import DeleteTodoUseCase
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from tests.factory.todo_factory import TodoFactory


class TestDeleteTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        todo_repository: SqliteTodoRepository,
        delete_todo_use_case: DeleteTodoUseCase,
        todo_factory: TodoFactory,
    ) -> None:
        self.todo_repository: TodoRepositoryPort = todo_repository
        self.delete_todo_use_case: DeleteTodoUseCase = delete_todo_use_case
        self.todo: TodoEntity = todo_factory.build()

    def test_deletes_existing_todo(self) -> None:
        # GIVEN
        self.todo_repository.save(self.todo)
        command = DeleteTodoCommand(todo_id=self.todo.id)

        # WHEN
        result: Result[None, DomainError] = self.delete_todo_use_case(command)
        persisted_todo = self.todo_repository.get_by_id(self.todo.id)

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_err is True
        assert isinstance(persisted_todo.error, TodoNotFoundError)

    def test_returns_not_found_error_for_missing_todo(self) -> None:
        # GIVEN
        command = DeleteTodoCommand(todo_id="missing-todo")

        # WHEN
        result: Result[None, DomainError] = self.delete_todo_use_case(command)

        # THEN
        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
