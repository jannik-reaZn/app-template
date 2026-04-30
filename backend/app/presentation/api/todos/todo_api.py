from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.presentation.api.routes import ApiRoute
from app.presentation.api.tags import ApiTag
from app.presentation.api.todos.create_todo_request import CreateTodoRequest
from app.presentation.api.todos.dependencies import (
    get_create_todo_use_case,
    get_get_todo_use_case,
)
from app.presentation.api.todos.todo_response import TodoResponse
from app.todos.application.create_todo_use_case import CreateTodoUseCase
from app.todos.application.get_todo_use_case import GetTodoUseCase

router = APIRouter(tags=[ApiTag.TODOS])


@router.post(
    ApiRoute.TODOS, response_model=TodoResponse, status_code=status.HTTP_201_CREATED
)
def create_todo(
    request: CreateTodoRequest,
    create_todo_use_case: Annotated[
        CreateTodoUseCase, Depends(get_create_todo_use_case)
    ],
) -> TodoResponse:
    result = create_todo_use_case.execute(title=request.title)
    if result.is_err:
        raise result.error
    return TodoResponse(
        id=result.value.id, title=result.value.title, status=result.value.status
    )


@router.get(
    ApiRoute.TODO_BY_ID, response_model=TodoResponse, status_code=status.HTTP_200_OK
)
def get_todo(
    todo_id: str,
    get_todo_use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)],
) -> TodoResponse:
    result = get_todo_use_case.execute(todo_id)
    if result.is_err:
        raise result.error
    return TodoResponse(
        id=result.value.id,
        title=result.value.title,
        status=result.value.status,
    )
