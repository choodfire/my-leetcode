from sqlalchemy.ext.asyncio import AsyncSession

from src.users import models, schemas


async def register(session: AsyncSession, user_create: schemas.UserCreate) -> models.User:
    user = models.User(
        **{
            "username": user_create.username,
            "email": user_create.email,
            "first_name": user_create.first_name,
            "last_name": user_create.last_name,
            "password": user_create.password,  # TODO: Encrypt
            "is_active": True,
            "is_admin": False,
        }
    )
    session.add(user)
    await session.commit()
    return user
