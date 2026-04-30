import pytest

from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.domain.entities import Todo
from app.todos.domain.errors import TodoNotFoundError
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository


class TestGetTodoUseCase:
    @pytest.fixture(autouse=True)
    def setup(
        self,
        todo_repository: InMemoryTodoRepository,
        get_todo_use_case: GetTodoUseCase,
    ) -> None:
        self.todo_repository = todo_repository
        self.get_todo_use_case = get_todo_use_case

    def test_returns_existing_todo(self) -> None:
        todo = Todo.create(todo_id="todo-123", title="Pay electricity bill").value
        self.todo_repository.save(todo)

        result = self.get_todo_use_case.execute("todo-123")

        assert result.is_ok is True
        assert result.value.id == "todo-123"
        assert result.value.title == "Pay electricity bill"
        assert result.value.status == "pending"

    def test_returns_not_found_error(self) -> None:
        result = self.get_todo_use_case.execute("missing-todo")

        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
