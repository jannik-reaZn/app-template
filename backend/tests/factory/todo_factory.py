from polyfactory.factories.dataclass_factory import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from app.todos.domain.entities import Todo


@register_fixture
class TodoFactory(DataclassFactory[Todo]):
    __model__ = Todo
    __use_examples__ = True
