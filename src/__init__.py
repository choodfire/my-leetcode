from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.database import sessionmanager
from src.models import Base
from src.results.router import router as results_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    async with sessionmanager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown


def create_app() -> FastAPI:
    init_data = {
        "lifespan": lifespan,
        "title": "Budget Leetcode",
        "redoc_url": None
    }

    app = FastAPI(**init_data)
    app.include_router(results_router)
    app.include_router(auth_router)

    return app
