from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from app.todos.domain.todo_entity import Todo


@register_fixture
class TodoFactory(ModelFactory[Todo]):
    __model__ = Todo
    __use_examples__ = True
