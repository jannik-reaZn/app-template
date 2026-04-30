from __future__ import annotations

from fastapi import APIRouter, status

from app.todos.application.create_todo import CreateTodoUseCase
from app.todos.infrastructure.in_memory_repository import (
    InMemoryTodoRepository,
    SequentialTodoIdGenerator,
)
from app.presentation.api.todos.create_todo_request import CreateTodoRequest
from app.presentation.api.todos.todo_response import TodoResponse

router = APIRouter()

todo_repository = InMemoryTodoRepository()
todo_id_generator = SequentialTodoIdGenerator()
create_todo_use_case = CreateTodoUseCase(todo_repository, todo_id_generator)


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(request: CreateTodoRequest) -> TodoResponse:
    result = create_todo_use_case.execute(title=request.title)
    if result.is_err:
        raise result.error
    return TodoResponse(
        id=result.value.id, title=result.value.title, status=result.value.status
    )
