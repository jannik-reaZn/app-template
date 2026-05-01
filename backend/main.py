from fastapi import FastAPI

from app.presentation.api.todos.todo_api import router as todo_router
from app.presentation.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
app.include_router(todo_router, prefix="/api")
