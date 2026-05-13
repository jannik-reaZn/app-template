from __future__ import annotations

from pydantic import Field

from app.core import DomainModel


class TodoTag(DomainModel):
    name: str = Field(
        title="Todo tag name",
        description="A label that can be shared across many todo items.",
        examples=["groceries"],
    )
