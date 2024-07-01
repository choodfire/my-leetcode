from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import services
from src.database import sessionmanager
from src.users import models, schemas

router = APIRouter(tags=["auth"])


@router.post("/register/", response_model=schemas.UserRead)
async def register(
    user_create: schemas.UserCreate,
    session: AsyncSession = Depends(sessionmanager.get_scoped_session),
) -> models.User:
    return await services.register(session=session, user_create=user_create)
