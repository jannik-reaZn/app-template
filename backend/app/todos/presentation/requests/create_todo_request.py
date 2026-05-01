from app.core import BaseSchema


class CreateTodoRequest(BaseSchema):
    title: str
