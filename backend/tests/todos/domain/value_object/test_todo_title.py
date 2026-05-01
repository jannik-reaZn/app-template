import pytest

from app.todos.domain.errors.todo_errors import EmptyTodoTitleError
from app.todos.domain.value_objects.todo_title import TodoTitle


class TestTodoTitle:
    def test_create_normalizes_whitespace(self) -> None:
        # WHEN
        title = TodoTitle.create("  Pay electricity bill  ")

        # THEN
        assert title.is_ok is True
        assert title.value.value == "Pay electricity bill"

    @pytest.mark.parametrize("raw_title", ["", "   "])
    def test_create_rejects_blank_title(self, raw_title: str) -> None:
        # WHEN
        title = TodoTitle.create(raw_title)

        # THEN
        assert title.is_err is True
        assert isinstance(title.error, EmptyTodoTitleError)
