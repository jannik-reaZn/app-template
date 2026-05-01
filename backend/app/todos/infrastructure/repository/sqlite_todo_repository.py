from __future__ import annotations

from sqlalchemy.orm import Session

from app.core import DomainError, Result
from app.core.database.sqlite import SqliteSession
from app.todos.domain.entities.todo_entity import Todo
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository import TodoRepository
from app.todos.infrastructure.database.todo_model import TodoRecord


class SqliteTodoRepository(TodoRepository):
    def __init__(self, session: SqliteSession) -> None:
        self.session: Session = session.session

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        todo_record = self.session.get(TodoRecord, todo_id)
        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(todo_record.to_domain())

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.session.merge(TodoRecord.from_domain(todo))
        self.session.commit()
        return Result.ok(todo)
