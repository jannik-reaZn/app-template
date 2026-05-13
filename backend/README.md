# Backend

## Database migrations

Alembic is configured in this backend and uses the application settings from [settings.py](settings.py).

Common commands:

```bash
cd backend
uv run alembic upgrade head
uv run alembic downgrade -1
uv run alembic revision --autogenerate -m "describe change"
```

The default database target is `backend/todos.db`. You can override it with `APP_DATABASE__TODO_DB_PATH`.
uv run alembic upgrade head
