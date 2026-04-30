from __future__ import annotations

from itertools import count


class SequentialTodoIdGenerator:
    def __init__(self) -> None:
        self._sequence = count(1)

    def new(self) -> str:
        return f"todo-{next(self._sequence)}"
