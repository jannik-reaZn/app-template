import pytest

from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository
from tests.factory.todo_factory import TodoFactory


class TestGetTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        todo_repository: InMemoryTodoRepository,
        get_todo_use_case: GetTodoUseCase,
        todo_factory: TodoFactory,
    ) -> None:
        self.todo_repository = todo_repository
        self.get_todo_use_case = get_todo_use_case
        self.todo = todo_factory.build()

    def test_returns_existing_todo(self) -> None:
        self.todo_repository.save(self.todo)

        result = self.get_todo_use_case.execute(self.todo.id)

        assert result.is_ok is True
        assert result.value.id == self.todo.id
        assert result.value.title == self.todo.title
        assert result.value.status == self.todo.status

    def test_returns_not_found_error(self) -> None:
        result = self.get_todo_use_case.execute("missing-todo")

        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
