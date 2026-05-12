import pytest

from app.core import DomainError, Result
from app.todos.application.queries.get_todo_query import GetTodoQuery
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.repository.sqlite_todo_repository import (
    SqliteTodoRepository,
)
from tests.factory.todo_factory import TodoFactory


class TestGetTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        todo_repository: SqliteTodoRepository,
        get_todo_use_case: GetTodoUseCase,
        todo_factory: TodoFactory,
    ) -> None:
        self.todo_repository: TodoRepositoryPort = todo_repository
        self.get_todo_use_case: GetTodoUseCase = get_todo_use_case
        self.todo: TodoEntity = todo_factory.build()

    def test_returns_existing_todo(self) -> None:
        # GIVEN
        self.todo_repository.save(self.todo)
        query = GetTodoQuery(todo_id=self.todo.id)

        # WHEN
        todo: Result[TodoEntity, DomainError] = self.get_todo_use_case(query)

        # THEN
        assert todo.is_ok is True
        assert todo.value.id == self.todo.id
        assert todo.value.title == self.todo.title
        assert todo.value.status == self.todo.status

    def test_returns_not_found_error(self) -> None:
        # GIVEN
        missing_todo_id: str = "missing-todo"
        query = GetTodoQuery(todo_id=missing_todo_id)

        # WHEN
        todo: Result[TodoEntity, DomainError] = self.get_todo_use_case(query)

        # THEN
        assert todo.is_err is True
        assert isinstance(todo.error, TodoNotFoundError)
