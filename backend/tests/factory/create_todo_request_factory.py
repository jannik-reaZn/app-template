from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from app.todos.presentation.requests.create_todo_request import CreateTodoRequest


@register_fixture
class CreateTodoRequestFactory(ModelFactory[CreateTodoRequest]):
    __model__ = CreateTodoRequest
    __use_examples__ = True
