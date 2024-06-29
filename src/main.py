from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.auth import models  # noqa: F401
from src.database import engine
from src.models import Base
from src.results import models  # noqa: F401, F811  # Will be fixed with router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index() -> dict:
    return {"Response": "Hello, World!"}
