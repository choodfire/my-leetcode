from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import utils
from src.users import models, schemas


async def register(session: AsyncSession, user_create: schemas.UserCreate) -> models.User:
    user = models.User(
        **{
            "username": user_create.username,
            "first_name": user_create.first_name,
            "last_name": user_create.last_name,
            "password": utils.encode_password(user_create.password),
            "is_active": True,
            "is_admin": False,
        }
    )
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(username: str, session: AsyncSession) -> models.User | None:
    stmt = select(models.User).filter(models.User.username == username)
    result = await session.execute(stmt)
    user = result.scalars().first()

    return user
