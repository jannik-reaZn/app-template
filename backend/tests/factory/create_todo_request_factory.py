from polyfactory.pytest_plugin import register_fixture

from app.todos.presentation.requests.create_todo_request import CreateTodoRequest
from tests.factory.base_pydantic_factory import BasePydanticFactory


@register_fixture
class CreateTodoRequestFactory(BasePydanticFactory[CreateTodoRequest]):
    __model__ = CreateTodoRequest
