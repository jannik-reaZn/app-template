from __future__ import annotations

from app.core import DomainError, Result
from app.todos.domain.todo_entity import Todo
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.domain.todo_repository import TodoRepository
from app.todos.infrastructure.database.session import SqliteSession
from app.todos.infrastructure.database.todo_model import TodoRecord


class SqliteTodoRepository(TodoRepository):
    def __init__(self, session: SqliteSession) -> None:
        self.session = session

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        todo_record = self.session.session.get(TodoRecord, todo_id)
        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(todo_record.to_domain())

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.session.session.merge(
            TodoRecord(id=todo.id, title=todo.title, status=todo.status)
        )
        self.session.session.commit()
        return Result.ok(todo)
