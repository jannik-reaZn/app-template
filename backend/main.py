from fastapi import FastAPI

from app.todos.presentation.api.todos.todo_api import router as todo_router
from app.todos.presentation.exception_handlers import register_exception_handlers
from settings import settings

app = FastAPI(title=settings.app.title)
register_exception_handlers(app)
app.include_router(todo_router, prefix=settings.app.api_prefix)
