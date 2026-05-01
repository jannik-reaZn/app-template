from __future__ import annotations

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSession:
    def __init__(
        self,
        metadata: MetaData,
        database_url: str,
        *,
        connect_args: dict[str, object] | None = None,
    ) -> None:
        self.engine = create_engine(
            database_url,
            connect_args=connect_args or {},
        )
        session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session: Session = session_factory()
        self._create_schema(metadata)

    def _create_schema(self, metadata: MetaData) -> None:
        metadata.create_all(self.engine)

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()
