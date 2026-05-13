from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.todos.application.commands.delete_todo_command import DeleteTodoCommand
from app.todos.application.queries.get_todo_query import GetTodoQuery
from app.todos.application.use_cases.create_todo_use_case import CreateTodoUseCase
from app.todos.application.use_cases.delete_todo_use_case import DeleteTodoUseCase
from app.todos.application.use_cases.get_todo_use_case import GetTodoUseCase
from app.todos.presentation.dependencies.todo_dependencies import (
    get_create_todo_use_case,
    get_delete_todo_use_case,
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
    return todo_presenter.present(create_todo_use_case(request.to_command()))


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
    return todo_presenter.present(get_todo_use_case(GetTodoQuery(todo_id=todo_id)))


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: str,
    delete_todo_use_case: Annotated[
        DeleteTodoUseCase, Depends(get_delete_todo_use_case)
    ],
) -> Response:
    result = delete_todo_use_case(DeleteTodoCommand(todo_id=todo_id))
    if result.is_err:
        raise result.error

    return Response(status_code=status.HTTP_204_NO_CONTENT)
