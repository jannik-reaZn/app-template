from __future__ import annotations

from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.enums.todo_status import TodoStatus
from app.todos.domain.value_objects.todo_title import TodoTitle
from app.todos.infrastructure.database.todo_model import TodoRecord


class TodoRecordMapper:
    @staticmethod
    def to_record(todo: TodoEntity) -> TodoRecord:
        return TodoRecord(todo_id=todo.id, title=todo.title.value, status=todo.status)

    @staticmethod
    def to_domain(todo_record: TodoRecord) -> TodoEntity:
        return TodoEntity(
            id=todo_record.todo_id,
            title=TodoTitle(value=todo_record.title),
            status=TodoStatus(todo_record.status),
        )
