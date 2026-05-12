from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.presentation.dependencies.todo_dependencies import (
    get_create_todo_use_case,
    get_get_todo_use_case,
    get_todo_presenter,
)
from app.todos.presentation.requests.create_todo_request import CreateTodoRequest
from app.todos.presentation.responses.todo_response import TodoResponse
from app.todos.presentation.todo_presenter import TodoPresenter

router = APIRouter(tags=["todos"])


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    request: CreateTodoRequest,
    create_todo_use_case: Annotated[
        CreateTodoUseCase, Depends(get_create_todo_use_case)
    ],
    todo_presenter: Annotated[TodoPresenter, Depends(get_todo_presenter)],
) -> TodoResponse:
    return todo_presenter.present(create_todo_use_case(title=request.title))


@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
def get_todo(
    todo_id: str,
    get_todo_use_case: Annotated[GetTodoUseCase, Depends(get_get_todo_use_case)],
    todo_presenter: Annotated[TodoPresenter, Depends(get_todo_presenter)],
) -> TodoResponse:
    return todo_presenter.present(get_todo_use_case(todo_id))
