from app.todos.application.get_todo_use_case import GetTodoUseCase
from app.todos.domain.entities import Todo
from app.todos.domain.errors import TodoNotFoundError
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository


def test_get_todo_use_case_returns_existing_todo() -> None:
    repository = InMemoryTodoRepository()
    todo = Todo.create(todo_id="todo-123", title="Pay electricity bill").value
    repository.save(todo)
    use_case = GetTodoUseCase(repository)

    result = use_case.execute("todo-123")

    assert result.is_ok is True
    assert result.value.id == "todo-123"
    assert result.value.title == "Pay electricity bill"
    assert result.value.status == "pending"


def test_get_todo_use_case_returns_not_found_error() -> None:
    use_case = GetTodoUseCase(InMemoryTodoRepository())

    result = use_case.execute("missing-todo")

    assert result.is_err is True
    assert isinstance(result.error, TodoNotFoundError)
