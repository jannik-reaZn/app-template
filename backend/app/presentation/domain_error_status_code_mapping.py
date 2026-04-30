from __future__ import annotations

from app.core import DomainError
from app.todos.domain.errors import TodoNotFoundError

type DomainErrorType = type[DomainError]

DOMAIN_ERROR_STATUS_CODES: dict[DomainErrorType, int] = {
    TodoNotFoundError: 404,
}
