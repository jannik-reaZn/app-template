from __future__ import annotations

from pathlib import Path

from app.core.database import DatabaseSession
from app.todos.infrastructure.database.todo_model import Base
from settings import settings


class SqliteSession(DatabaseSession):
    def __init__(
        self,
        database_path: str | Path = settings.database.todo_db_path,
    ) -> None:
        super().__init__(
            metadata=Base.metadata,
            database_url=self._build_database_url(database_path),
            connect_args=settings.database.connect_args,
        )

    @staticmethod
    def _build_database_url(database_path: str | Path) -> str:
        if database_path == settings.database.in_memory_path:
            return settings.database.in_memory_url
        return f"{settings.database.url_prefix}{Path(database_path).resolve()}"
