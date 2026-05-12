from app.presentation.base_schema import BaseSchema


class CreateTodoRequest(BaseSchema):
    title: str
