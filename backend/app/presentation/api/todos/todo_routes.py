from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.todos.application.create_todo import CreateTodoUseCase
from app.presentation.api.todos.dependencies import get_create_todo_use_case
from app.presentation.api.todos.create_todo_request import CreateTodoRequest
from app.presentation.api.todos.todo_response import TodoResponse

router = APIRouter()


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
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
