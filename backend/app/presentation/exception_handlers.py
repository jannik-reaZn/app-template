from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core import DomainError
from app.presentation.domain_error_statuses import get_domain_error_status


async def handle_domain_error(
    _: Request,
    exc: Exception,
) -> JSONResponse:
    domain_error = cast(DomainError, exc)
    return JSONResponse(
        status_code=get_domain_error_status(domain_error),
        content={"detail": str(domain_error)},
    )


async def handle_validation_error(
    _: Request,
    exc: Exception,
) -> JSONResponse:
    validation_error = cast(ValidationError, exc)
    return JSONResponse(
        status_code=422,
        content={"detail": validation_error.errors()},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, handle_domain_error)
    app.add_exception_handler(ValidationError, handle_validation_error)
