from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: str
    title: str
    status: str
