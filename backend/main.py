from fastapi import FastAPI

from app.presentation.api.todo_routes import router as todo_router

app = FastAPI()
app.include_router(todo_router, prefix="/api")
