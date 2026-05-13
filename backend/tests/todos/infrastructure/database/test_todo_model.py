from app.todos.domain.entities.todo_entity import TodoEntity
from app.todos.domain.value_objects.todo_note import TodoNote
from app.todos.infrastructure.database.todo_mapper import TodoRecordMapper
from app.todos.infrastructure.database.todo_model import TodoNoteRecord, TodoRecord
from tests.factory.todo_factory import TodoFactory
from tests.factory.todo_record_factory import TodoRecordFactory


class TestTodoRecord:
    def test_mapper_to_record_maps_domain_fields_to_record(self) -> None:
        # GIVEN
        todo: TodoEntity = TodoFactory.build(
            notes=(
                TodoNote(content="Buy oat milk"),
                TodoNote(content="Check pantry first"),
            )
        )

        # WHEN
        record: TodoRecord = TodoRecordMapper.to_record(todo)

        # THEN
        assert record.todo_id == todo.id
        assert record.title == todo.title.value
        assert record.status == todo.status
        assert [note.content for note in record.notes] == [
            "Buy oat milk",
            "Check pantry first",
        ]

    def test_mapper_to_domain_maps_record_fields_to_domain(self) -> None:
        # GIVEN
        record: TodoRecord = TodoRecordFactory.build()
        record.notes = [
            TodoNoteRecord(content="Buy oat milk", position=0),
            TodoNoteRecord(content="Check pantry first", position=1),
        ]

        # WHEN
        todo: TodoEntity = TodoRecordMapper.to_domain(record)

        # THEN
        assert todo.id == record.todo_id
        assert todo.title.value == record.title
        assert todo.status == record.status
        assert [note.content for note in todo.notes] == [
            "Buy oat milk",
            "Check pantry first",
        ]
