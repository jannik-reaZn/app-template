from __future__ import annotations

from enum import StrEnum


class TodoRepositoryType(StrEnum):
    SQLITE = "sqlite"
    IN_MEMORY = "in-memory"
