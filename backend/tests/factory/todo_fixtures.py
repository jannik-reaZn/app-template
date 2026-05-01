import pytest

from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository


@pytest.fixture
def todo_repository() -> InMemoryTodoRepository:
    return InMemoryTodoRepository()


@pytest.fixture
def create_todo_use_case() -> CreateTodoUseCase:
    return CreateTodoUseCase(InMemoryTodoRepository())


@pytest.fixture
def get_todo_use_case(todo_repository: InMemoryTodoRepository) -> GetTodoUseCase:
    return GetTodoUseCase(todo_repository)
