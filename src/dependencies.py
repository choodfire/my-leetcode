from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.consts import JWTTokenType
from src.auth.dependencies import get_token_payload
from src.database import sessionmanager
from src.users import models


async def get_user(
    session: AsyncSession = Depends(sessionmanager.session),
    payload: dict = Depends(get_token_payload),
) -> models.User:
    user_id: str | None = payload.get("sub")

    if payload["type"] != JWTTokenType.ACCESS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    stmt = select(models.User).filter(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user.username != payload.get("username"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user
