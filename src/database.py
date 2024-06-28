from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(
    settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,  # TODO: Remove in future
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
