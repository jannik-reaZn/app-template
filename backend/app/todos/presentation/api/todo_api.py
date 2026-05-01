from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.presentation.dependencies.todo_dependencies import (
    get_create_todo_use_case,
    get_get_todo_use_case,
)
from app.todos.presentation.requests.create_todo_request import CreateTodoRequest
from app.todos.presentation.responses.todo_response import TodoResponse

router = APIRouter(tags=["todos"])


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    request: CreateTodoRequest,
    create_todo_use_case: Annotated[
        CreateTodoUseCase, Depends(get_create_todo_use_case)
    ],
) -> TodoResponse:
    result = create_todo_use_case(title=request.title)
    if result.is_err:
        raise result.error
    return TodoResponse(
        id=result.value.id, title=result.value.title, status=result.value.status
    )


@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
def get_todo(
    todo_id: str,
    get_todo_use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)],
) -> TodoResponse:
    result = get_todo_use_case(todo_id)
    if result.is_err:
        raise result.error
    return TodoResponse(
        id=result.value.id,
        title=result.value.title,
        status=result.value.status,
    )
