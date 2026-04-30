from app.core import BaseSchema


class TodoResponse(BaseSchema):
    id: str
    title: str
    status: str
