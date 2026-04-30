from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.todos.application.create_todo import CreateTodoUseCase
from app.todos.domain.errors import DomainError, EmptyTodoTitleError
from app.todos.infrastructure.in_memory_repository import (
    InMemoryTodoRepository,
    SequentialTodoIdGenerator,
)
from app.presentation.api.schemas import CreateTodoRequest, TodoResponse

router = APIRouter()

todo_repository = InMemoryTodoRepository()
todo_id_generator = SequentialTodoIdGenerator()
create_todo_use_case = CreateTodoUseCase(todo_repository, todo_id_generator)


def map_error_to_http(error: DomainError) -> None:
    if isinstance(error, EmptyTodoTitleError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todo title cannot be empty",
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected error",
    )


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(request: CreateTodoRequest) -> TodoResponse:
    result = create_todo_use_case.execute(title=request.title)
    if result.is_err:
        map_error_to_http(result.error)
    return TodoResponse(
        id=result.value.id, title=result.value.title, status=result.value.status
    )
