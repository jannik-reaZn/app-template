from app.todos.domain.todo_entity import Todo
from app.todos.infrastructure.database.todo_model import TodoRecord
from tests.factory.todo_factory import TodoFactory
from tests.factory.todo_record_factory import TodoRecordFactory


class TestTodoRecord:
    def test_from_domain_maps_domain_fields_to_record(self) -> None:
        # GIVEN
        todo: Todo = TodoFactory.build()

        # WHEN
        record: TodoRecord = TodoRecord.from_domain(todo)

        # THEN
        assert record.id == todo.id
        assert record.title == todo.title
        assert record.status == todo.status

    def test_to_domain_maps_record_fields_to_domain(self) -> None:
        # GIVEN
        record: TodoRecord = TodoRecordFactory.build()

        # WHEN
        todo: Todo = record.to_domain()

        # THEN
        assert todo.id == record.id
        assert todo.title == record.title
        assert todo.status == record.status
