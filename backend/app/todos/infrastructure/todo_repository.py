from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core import DomainError, Result
from app.todos.domain.todo_entity import Todo
from app.todos.domain.todo_errors import TodoNotFoundError
from app.todos.domain.todo_repository import TodoRepository

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TODO_DB_PATH = WORKSPACE_ROOT / "todos.db"


class SqliteSession:
    def __init__(self, database_path: str | Path = DEFAULT_TODO_DB_PATH) -> None:
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def _create_schema(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()


class SqliteTodoRepository(TodoRepository):
    def __init__(self, session: SqliteSession) -> None:
        self.session = session

    def get_by_id(self, todo_id: str) -> Result[Todo, DomainError]:
        row = self.session.connection.execute(
            "SELECT id, title, status FROM todos WHERE id = ?",
            (todo_id,),
        ).fetchone()
        if row is None:
            return Result.err(TodoNotFoundError(todo_id))
        return Result.ok(Todo(id=row["id"], title=row["title"], status=row["status"]))

    def save(self, todo: Todo) -> Result[Todo, DomainError]:
        self.session.connection.execute(
            """
            INSERT INTO todos (id, title, status)
            VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                status = excluded.status
            """,
            (todo.id, todo.title, todo.status),
        )
        self.session.connection.commit()
        return Result.ok(todo)
