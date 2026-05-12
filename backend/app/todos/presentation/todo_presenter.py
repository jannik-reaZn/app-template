from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.presentation.responses.todo_response import TodoResponse


class TodoPresenter:
    def present(self, result: Result[TodoEntity, DomainError]) -> TodoResponse:
        if result.is_err:
            raise result.error

        todo = result.value
        return TodoResponse(
            id=todo.id,
            title=todo.title.value,
            status=todo.status,
        )
