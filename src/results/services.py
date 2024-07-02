from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import src.users.models
from src.results import models, schemas


async def get_results(session: AsyncSession) -> list[models.Result]:
    stmt = select(models.Result).order_by(models.Result.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def retrieve_result(session: AsyncSession, result_id: int) -> models.Result:
    res = await session.get(models.Result, result_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Result {result_id} not found!")
    return res


async def create_result(
    session: AsyncSession, result_create: schemas.ResultWrite, user: src.users.models.User
) -> models.Result:
    from datetime import timedelta

    result = models.Result(
        **result_create.model_dump(), user_id=user.id, time=timedelta(minutes=1, seconds=1)
    )  # TODO: Temporary
    session.add(result)
    await session.commit()
    return result
