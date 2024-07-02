from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import services, utils
from src.database import sessionmanager
from src.users import models, schemas


async def check_registration(
    user_create: schemas.UserCreate, session: AsyncSession = Depends(sessionmanager.get_scoped_session)
) -> schemas.UserCreate:
    if await services.get_user_by_username(user_create.username, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Пользователь с именем {user_create.username} уже существует"
        )

    return user_create  # TODO: Add validations


async def check_login(
    user_login: schemas.UserLogin, session: AsyncSession = Depends(sessionmanager.get_scoped_session)
) -> models.User:
    if not (user := await services.get_user_by_username(user_login.username, session)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Пользователя с именем {user_login.username} не существует"
        )

    if not utils.check_password(user_login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный пароль")

    return user
