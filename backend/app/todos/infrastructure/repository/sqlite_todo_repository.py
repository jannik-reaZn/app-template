from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import DomainError, Result
from app.infrastructure.database.sqlite import SqliteSession
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.infrastructure.database.todo_mapper import TodoRecordMapper
from app.todos.infrastructure.database.todo_model import TodoNoteRecord, TodoRecord


class SqliteTodoRepository(TodoRepositoryPort):
    def __init__(self, session: SqliteSession) -> None:
        self.session: Session = session.session

    def get_by_id(self, todo_id: str) -> Result[TodoEntity, DomainError]:
        statement = select(TodoRecord).where(TodoRecord.todo_id == todo_id)
        todo_record = self.session.scalar(statement)
        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(TodoRecordMapper.to_domain(todo_record))

    def save(self, todo: TodoEntity) -> Result[TodoEntity, DomainError]:
        statement = select(TodoRecord).where(TodoRecord.todo_id == todo.id)
        todo_record = self.session.scalar(statement)

        if todo_record is None:
            self.session.add(TodoRecordMapper.to_record(todo))
        else:
            todo_record.title = todo.title.value
            todo_record.status = todo.status
            todo_record.notes = [
                TodoNoteRecord(content=note.content, position=index)
                for index, note in enumerate(todo.notes)
            ]

        self.session.commit()
        return Result.ok(todo)
