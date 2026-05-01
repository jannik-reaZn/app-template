from __future__ import annotations

from pathlib import Path

from app.core.database import DatabaseSession
from app.todos.infrastructure.database.todo_model import Base

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_TODO_DB_PATH = WORKSPACE_ROOT / "todos.db"
SQLITE_IN_MEMORY_PATH = ":memory:"
SQLITE_IN_MEMORY_URL = "sqlite+pysqlite:///:memory:"
SQLITE_URL_PREFIX = "sqlite+pysqlite:///"
SQLITE_CONNECT_ARGS: dict[str, object] = {"check_same_thread": False}


class SqliteSession(DatabaseSession):
    def __init__(self, database_path: str | Path = DEFAULT_TODO_DB_PATH) -> None:
        super().__init__(
            metadata=Base.metadata,
            database_url=self._build_database_url(database_path),
            connect_args=SQLITE_CONNECT_ARGS,
        )

    @staticmethod
    def _build_database_url(database_path: str | Path) -> str:
        if database_path == SQLITE_IN_MEMORY_PATH:
            return SQLITE_IN_MEMORY_URL
        return f"{SQLITE_URL_PREFIX}{Path(database_path).resolve()}"
