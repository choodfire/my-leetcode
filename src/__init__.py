from contextlib import asynccontextmanager
from typing import AsyncGenerator
from alembic.config import Config
from alembic import command

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.database import sessionmanager
from src.models import Base
from src.results.router import router as results_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
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
