from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from app.todos.domain.entities.todo_entity import TodoEntity


@register_fixture
class TodoFactory(ModelFactory[TodoEntity]):
    __model__ = TodoEntity
    __use_examples__ = True
