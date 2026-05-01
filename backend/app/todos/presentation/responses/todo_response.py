from app.core import BaseSchema
from app.todos.domain.entities.todo_entity import TodoStatus


class TodoResponse(BaseSchema):
    id: str
    title: str
    status: TodoStatus
