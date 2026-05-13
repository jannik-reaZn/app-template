from __future__ import annotations

from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.enums.todo_status import TodoStatus
from app.todos.domain.value_objects.todo_note import TodoNote
from app.todos.domain.value_objects.todo_tag import TodoTag
from app.todos.domain.value_objects.todo_title import TodoTitle
from app.todos.infrastructure.database.todo_model import (
    TodoNoteRecord,
    TodoRecord,
    TodoTagLinkRecord,
    TodoTagRecord,
)


class TodoRecordMapper:
    @staticmethod
    def to_record(todo: TodoEntity) -> TodoRecord:
        return TodoRecord(
            todo_id=todo.id,
            title=todo.title.value,
            status=todo.status,
            notes=TodoRecordMapper.to_note_records(todo.notes),
            tag_links=TodoRecordMapper.to_tag_links(todo.tags),
        )

    @staticmethod
    def to_note_records(notes: tuple[TodoNote, ...]) -> list[TodoNoteRecord]:
        return [
            TodoNoteRecord(content=note.content, position=index)
            for index, note in enumerate(notes)
        ]

    @staticmethod
    def to_tag_links(tags: tuple[TodoTag, ...]) -> list[TodoTagLinkRecord]:
        return [TodoTagLinkRecord(tag_name=tag.name) for tag in tags]

    @staticmethod
    def to_domain(todo_record: TodoRecord) -> TodoEntity:
        return TodoEntity(
            id=todo_record.todo_id,
            title=TodoTitle(value=todo_record.title),
            status=TodoStatus(todo_record.status),
            notes=tuple(
                TodoNote(content=note_record.content)
                for note_record in todo_record.notes
            ),
            tags=tuple(
                TodoTag(name=tag_link.tag_name) for tag_link in todo_record.tag_links
            ),
        )
