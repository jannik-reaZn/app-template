from pydantic import Field

from app.presentation.base_schema import BaseSchema
from app.todos.application.commands.create_todo_command import CreateTodoCommand


class CreateTodoRequest(BaseSchema):
    title: str
    notes: list[str] = Field(default_factory=list)

    def to_command(self) -> CreateTodoCommand:
        return CreateTodoCommand(title=self.title, notes=tuple(self.notes))
