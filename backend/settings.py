from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent


class AppSettings(BaseModel):
    title: str = "Application Template"
    api_prefix: str = "/api"
    mcp_name: str = "Application Template Reference MCP"


class DatabaseSettings(BaseModel):
    todo_db_path: Path = BACKEND_ROOT / "todos.db"
    in_memory_path: str = ":memory:"
    in_memory_url: str = "sqlite+pysqlite:///:memory:"
    url_prefix: str = "sqlite+pysqlite:///"
    connect_args: dict[str, object] = {"check_same_thread": False}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
