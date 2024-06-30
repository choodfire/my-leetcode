from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.auth import models  # noqa: F401
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


app = FastAPI(lifespan=lifespan)
app.include_router(results_router)


@app.get("/")
def index() -> dict:
    return {"Response": "Hello, World!"}
