from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from app.core import DomainError, Result
from app.infrastructure.database.sqlite import SqliteSession
from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.errors.todo_errors import TodoNotFoundError
from app.todos.domain.interfaces.todo_repository_port import TodoRepositoryPort
from app.todos.domain.value_objects.todo_tag import TodoTag
from app.todos.infrastructure.database.todo_mapper import TodoRecordMapper
from app.todos.infrastructure.database.todo_model import (
    TodoRecord,
    TodoTagRecord,
)


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
            self._create(todo)
        else:
            self._update(todo_record, todo)

        self.session.commit()
        return Result.ok(todo)

    def delete(self, todo_id: str) -> Result[None, DomainError]:
        statement = select(TodoRecord).where(TodoRecord.todo_id == todo_id)
        todo_record = self.session.scalar(statement)

        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))

        self.session.delete(todo_record)
        self.session.commit()
        return Result.ok(None)

    def _create(self, todo: TodoEntity) -> None:
        self._ensure_tags_exist(todo.tags)
        self.session.add(TodoRecordMapper.to_record(todo))

    def _update(self, todo_record: TodoRecord, todo: TodoEntity) -> None:
        self._ensure_tags_exist(todo.tags)
        todo_record.title = todo.title.value
        todo_record.status = todo.status
        todo_record.notes = TodoRecordMapper.to_note_records(todo.notes)
        todo_record.tag_links = TodoRecordMapper.to_tag_links(todo.tags)

    def _ensure_tags_exist(self, tags: tuple[TodoTag, ...]) -> None:
        tag_names = tuple(dict.fromkeys(tag.name for tag in tags))
        if not tag_names:
            return

        statement = insert(TodoTagRecord).values(
            [{"name": tag_name} for tag_name in tag_names]
        )
        self.session.execute(statement.on_conflict_do_nothing(index_elements=["name"]))
