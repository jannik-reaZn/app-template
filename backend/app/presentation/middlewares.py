from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from app.core import DomainError
from app.todos.domain.errors import TodoNotFoundError


async def handle_domain_errors(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    try:
        return await call_next(request)
    except DomainError as exc:
        if isinstance(exc, TodoNotFoundError):
            return JSONResponse(status_code=404, content={"detail": str(exc)})
        return JSONResponse(status_code=400, content={"detail": str(exc)})


def register_middlewares(app: FastAPI) -> None:
    app.middleware("http")(handle_domain_errors)
