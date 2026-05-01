from __future__ import annotations

from pathlib import Path

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.core import DomainError, Result
from app.todos.domain.todo_entity import Todo, TodoStatus
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.domain.todo_repository import TodoRepository

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TODO_DB_PATH = WORKSPACE_ROOT / "todos.db"


class Base(DeclarativeBase):
    pass


class TodoRecord(Base):
    __tablename__ = "todos"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)


class SqliteSession:
    def __init__(self, database_path: str | Path = DEFAULT_TODO_DB_PATH) -> None:
        self.engine = create_engine(
            self._build_database_url(database_path),
            connect_args={"check_same_thread": False},
        )
        session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = session_factory()
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


class SqliteTodoRepository(TodoRepository):
    def __init__(self, session: SqliteSession) -> None:
        self.session = session

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        todo_record = self.session.session.get(TodoRecord, todo_id)
        if todo_record is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(
            Todo(
                id=todo_record.id,
                title=todo_record.title,
                status=TodoStatus(todo_record.status),
            )
        )

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.session.session.merge(
            TodoRecord(id=todo.id, title=todo.title, status=todo.status)
        )
        self.session.session.commit()
        return Result.ok(todo)
