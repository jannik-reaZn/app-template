from uuid import UUID

from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.enums.todo_status import TodoStatus
from app.todos.domain.errors.todo_errors import EmptyTodoTitleError


class TestTodo:
    def test_create_returns_todo_with_normalized_title(self) -> None:
        # WHEN
        todo = TodoEntity.create(
            "  Pay electricity bill  ", status=TodoStatus.COMPLETED
        )

        # THEN
        assert todo.is_ok is True
        assert UUID(todo.value.id)
        assert todo.value.title.value == "Pay electricity bill"
        assert todo.value.status == TodoStatus.COMPLETED

    def test_create_returns_error_for_blank_title(self) -> None:
        # WHEN
        todo = TodoEntity.create("   ")

        # THEN
        assert todo.is_err is True
        assert isinstance(todo.error, EmptyTodoTitleError)
