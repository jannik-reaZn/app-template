from __future__ import annotations

from app.core import DomainError
from app.todos.domain.todo_errors import EmptyTodoTitleError, TodoNotFoundError

type DomainErrorType = type[DomainError]

DOMAIN_ERROR_STATUS_CODES: dict[DomainErrorType, int] = {
    EmptyTodoTitleError: 400,
    TodoNotFoundError: 404,
}
