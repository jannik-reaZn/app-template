from polyfactory.pytest_plugin import register_fixture

from app.todos.domain.entities.todo_entity import TodoEntity
from tests.factory.base_pydantic_factory import BasePydanticFactory


@register_fixture
class TodoFactory(BasePydanticFactory[TodoEntity]):
    __model__ = TodoEntity
