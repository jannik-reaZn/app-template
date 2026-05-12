from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import DomainError, Result
from app.core.database.sqlite import SqliteSession
from app.todos.domain.entities.todo_entity import Todo
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.database.todo_model import TodoRecord


class SqliteTodoRepository(TodoRepositoryPort):
    def __init__(self, session: SqliteSession) -> None:
        self.session: Session = session.session

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        statement = select(TodoRecord).where(TodoRecord.todo_id == todo_id)
        todo_record = self.session.scalar(statement)
        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(todo_record.to_domain())

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        statement = select(TodoRecord).where(TodoRecord.todo_id == todo.id)
        todo_record = self.session.scalar(statement)

        if todo_record is None:
            self.session.add(TodoRecord.from_domain(todo))
        else:
            todo_record.title = todo.title.value
            todo_record.status = todo.status

        self.session.commit()
        return Result.ok(todo)
