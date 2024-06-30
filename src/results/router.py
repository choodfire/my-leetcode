from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import sessionmanager
from src.results.models import Result
from src.results.schemas import ResultRead

router = APIRouter(prefix="/results")


@router.get("/", response_model=list[ResultRead])
async def get_results(session: AsyncSession = Depends(sessionmanager.session)) -> list[Result]:
    stmt = select(Result).order_by(Result.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.get("/{result_id}", response_model=ResultRead)
async def get_result(result_id: int, session: AsyncSession = Depends(sessionmanager.session)) -> Result:
    res = await session.get(Result, result_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Result {result_id} not found!")
    return res
