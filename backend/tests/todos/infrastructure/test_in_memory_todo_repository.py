from app.todos.domain.todo_entity import Todo
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.infrastructure.repository import InMemoryTodoRepository


class TestInMemoryTodoRepository:
    def test_save_persists_todo(self) -> None:
        # GIVEN
        repository = InMemoryTodoRepository()
        todo = Todo.create(title="Pay electricity bill").value

        # WHEN
        result = repository.save(todo)
        persisted_todo = repository.get_by_id(todo.id)

        # THEN
        assert result.is_ok is True
        assert persisted_todo.is_ok is True
        assert persisted_todo.value == todo

    def test_get_by_id_returns_not_found_error_for_missing_todo(self) -> None:
        # GIVEN
        repository = InMemoryTodoRepository()

        # WHEN
        result = repository.get_by_id("missing-todo")

        # THEN
        assert result.is_err is True
        assert isinstance(result.error, TodoNotFoundError)
        assert result.error.todo_id == "missing-todo"
