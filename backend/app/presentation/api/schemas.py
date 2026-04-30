from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    title: str


class TodoResponse(BaseModel):
    id: str
    title: str
    status: str
