from fastapi import FastAPI

from app.presentation.api.todos.todo_api import router as todo_router
from app.presentation.middlewares import register_middlewares

app = FastAPI()
register_middlewares(app)
app.include_router(todo_router, prefix="/api")
