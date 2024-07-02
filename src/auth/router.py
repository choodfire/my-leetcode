from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import dependencies, services, utils
from src.auth.schemas import Token
from src.database import sessionmanager
from src.users import models, schemas

router = APIRouter(tags=["auth"])


@router.post("/register/", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: schemas.UserCreate = Depends(dependencies.check_registration),
    session: AsyncSession = Depends(sessionmanager.session),
) -> Token:
    user = await services.register(session=session, user_create=user_create)
    return await utils.create_auth_tokens(user)


@router.post("/login/", response_model=Token, status_code=status.HTTP_200_OK)
async def login(user: models.User = Depends(dependencies.check_login)) -> Token:
    return await utils.create_auth_tokens(user)
