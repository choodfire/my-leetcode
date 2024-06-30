from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


class DatabaseSessionManager:
    def __init__(self) -> None:
        self.engine = create_async_engine(
            settings.asyncpg_url.unicode_string(),
            future=True,
            echo=True,  # TODO: Remove in future
        )
        self.sessionmaker = async_sessionmaker(
            self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> AsyncSession:
        return async_scoped_session(
            session_factory=self.sessionmaker,
            scopefunc=current_task,
        )

    async def session(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            yield session
            await session.close()


sessionmanager = DatabaseSessionManager()
