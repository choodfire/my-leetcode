from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
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


bearer = HTTPBearer()


async def get_token_payload(token: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    return utils.decode_jwt(token=token.credentials)


async def get_user(
    session: AsyncSession = Depends(sessionmanager.get_scoped_session),
    payload: dict = Depends(get_token_payload),
) -> models.User:
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    stmt = select(models.User).filter(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user
