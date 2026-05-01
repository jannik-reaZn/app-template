from polyfactory.pytest_plugin import register_fixture

from tests.factory.todo_factory import TodoFactory
from tests.factory.todo_fixtures import (  # noqa: F401
    create_todo_use_case,
    get_todo_use_case,
    sqlite_session,
    todo_in_memory_repository,
    todo_repository,
)

register_fixture(TodoFactory)
