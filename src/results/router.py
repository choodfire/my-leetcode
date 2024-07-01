from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import sessionmanager
from src.results import models, schemas, service

router = APIRouter(prefix="/results", tags=["results"])


@router.get("/", response_model=list[schemas.ResultRead])
async def get_results(session: AsyncSession = Depends(sessionmanager.session)) -> list[models.Result]:
    return await service.get_results(session=session)


@router.get("/{result_id}", response_model=schemas.ResultRead)
async def retrieve_result(result_id: int, session: AsyncSession = Depends(sessionmanager.session)) -> models.Result:
    return await service.retrieve_result(session=session, result_id=result_id)


@router.post("/", response_model=schemas.ResultRead)
async def create_result(
    result_create: schemas.ResultWrite, session: AsyncSession = Depends(sessionmanager.session)
) -> models.Result:
    return await service.create_result(session=session, result_create=result_create)
