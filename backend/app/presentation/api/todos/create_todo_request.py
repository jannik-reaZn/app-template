from pydantic import BaseModel


class CreateTodoRequest(BaseModel):
    title: str
