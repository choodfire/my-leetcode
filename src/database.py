from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession, \
    async_scoped_session

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

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.sessionmaker,
            scopefunc=current_task,
        )
        return session

    async def session(self) -> AsyncSession:
        async with self.sessionmaker() as session:
            yield session
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_session():
    async with sessionmanager.session() as session:
        yield session
