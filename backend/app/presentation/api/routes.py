from enum import StrEnum


class ApiRoute(StrEnum):
    TODOS = "/todos"
    TODO_BY_ID = "/todos/{todo_id}"
