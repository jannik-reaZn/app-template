from collections.abc import Iterator

import pytest
from polyfactory.pytest_plugin import register_fixture

from app.core.database.base_model import Base
from app.core.database.sqlite import SqliteSession
from tests.factory.create_todo_request_factory import CreateTodoRequestFactory
from tests.factory.todo_factory import TodoFactory
from tests.factory.todo_fixtures import (  # noqa: F401
    create_todo_use_case,
    get_todo_use_case,
    todo_in_memory_repository,
    todo_repository,
)
from tests.factory.todo_record_factory import TodoRecordFactory


@pytest.fixture
def sqlite_session() -> Iterator[SqliteSession]:
    session = SqliteSession(metadata=Base.metadata, database_path=":memory:")
    yield session
    session.close()


register_fixture(CreateTodoRequestFactory)
register_fixture(TodoFactory)
register_fixture(TodoRecordFactory)
