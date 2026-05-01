from app.core import BaseSchema
from app.todos.domain.enum.todo_status import TodoStatus


class TodoResponse(BaseSchema):
    id: str
    title: str
    status: TodoStatus
