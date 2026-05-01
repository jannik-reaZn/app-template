from __future__ import annotations

from app.core import DomainError
from app.presentation.domain_error_status_code_mapping import (
    DOMAIN_ERROR_STATUS_CODES,
)

DEFAULT_DOMAIN_ERROR_STATUS_CODE = 400


def get_domain_error_status(error: DomainError) -> int:
    for error_type in type(error).__mro__:
        if not issubclass(error_type, DomainError):
            continue
        status_code = DOMAIN_ERROR_STATUS_CODES.get(error_type)
        if status_code is not None:
            return status_code
    return DEFAULT_DOMAIN_ERROR_STATUS_CODE
