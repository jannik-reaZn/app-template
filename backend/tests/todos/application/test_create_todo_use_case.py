from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.domain.errors import EmptyTodoTitleError
from app.todos.infrastructure.todo_repository import InMemoryTodoRepository


class StaticTodoIdGenerator:
    def new(self) -> str:
        return "todo-123"


def test_create_todo_use_case_returns_pending_todo() -> None:
    use_case = CreateTodoUseCase(InMemoryTodoRepository(), StaticTodoIdGenerator())

    result = use_case.execute(title="Pay electricity bill")

    assert result.is_ok is True
    assert result.value.id == "todo-123"
    assert result.value.title == "Pay electricity bill"
    assert result.value.status == "pending"


def test_create_todo_use_case_returns_error_for_blank_title() -> None:
    use_case = CreateTodoUseCase(InMemoryTodoRepository(), StaticTodoIdGenerator())

    result = use_case.execute(title="   ")

    assert result.is_err is True
    assert isinstance(result.error, EmptyTodoTitleError)
