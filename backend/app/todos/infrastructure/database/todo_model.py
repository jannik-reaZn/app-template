from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base_model import Base


class TodoRecord(Base):
    __tablename__ = "todos"

    todo_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
