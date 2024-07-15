from fastapi import Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import services, utils
from src.auth.consts import JWTTokenType
from src.database import sessionmanager
from src.users import models, schemas

oauth2 = OAuth2PasswordBearer(tokenUrl="/login/")


async def check_registration(
    user_create: schemas.UserCreate, session: AsyncSession = Depends(sessionmanager.session)
) -> schemas.UserCreate:
    if await services.get_user_by_username(user_create.username, session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Пользователь с именем {user_create.username} уже существует"
        )

    return user_create  # TODO: Add validations


async def check_login(
    username: str = Form(), password: str = Form(), session: AsyncSession = Depends(sessionmanager.session)
) -> models.User:
    if not (user := await services.get_user_by_username(username, session)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Пользователя с именем {username} не существует"
        )

    if not utils.check_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный пароль")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Запрещено")

    return user


async def get_token_payload(token: str = Depends(oauth2)) -> dict:
    try:
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from None

    return payload


async def get_user_from_refresh_token(
    session: AsyncSession = Depends(sessionmanager.session),
    payload: dict = Depends(get_token_payload),
) -> models.User:
    user_id: str | None = payload.get("sub")

    if payload["type"] != JWTTokenType.REFRESH:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

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
