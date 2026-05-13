from app.presentation.base_schema import BaseSchema
from app.todos.domain.enums.todo_status import TodoStatus


class TodoResponse(BaseSchema):
    id: str
    title: str
    status: TodoStatus
    notes: list[str]
    tags: list[str]
