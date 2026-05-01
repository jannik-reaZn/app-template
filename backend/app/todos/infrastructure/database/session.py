from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.todos.infrastructure.database.models import Base

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_TODO_DB_PATH = WORKSPACE_ROOT / "todos.db"


class SqliteSession:
    def __init__(self, database_path: str | Path = DEFAULT_TODO_DB_PATH) -> None:
        self.engine = create_engine(
            self._build_database_url(database_path),
            connect_args={"check_same_thread": False},
        )
        session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session: Session = session_factory()
        self._create_schema()

    @staticmethod
    def _build_database_url(database_path: str | Path) -> str:
        if database_path == ":memory:":
            return "sqlite+pysqlite:///:memory:"
        return f"sqlite+pysqlite:///{Path(database_path).resolve()}"

    def _create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()
