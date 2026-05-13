from __future__ import annotations

from pydantic import Field

from app.core import DomainModel


class TodoNote(DomainModel):
    content: str = Field(
        title="Todo note content",
        description="Additional detail attached to a todo item.",
        examples=["Buy oat milk"],
    )
