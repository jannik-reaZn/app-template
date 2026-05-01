from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.pytest_plugin import register_fixture

from app.todos.domain.enum.todo_status import TodoStatus
from app.todos.infrastructure.database.todo_model import TodoRecord


@register_fixture
class TodoRecordFactory(SQLAlchemyFactory[TodoRecord]):
    __model__ = TodoRecord
    status = TodoStatus.PENDING
