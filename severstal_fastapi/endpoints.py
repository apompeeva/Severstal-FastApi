from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from severstal_fastapi.database import get_async_session
from severstal_fastapi.service import SqlAlchemyDbService
from severstal_fastapi.schemas import CoilAdd, CoilDelete, StatsRange

router = APIRouter()


async def get_db_service(session: AsyncSession = Depends(get_async_session)) -> SqlAlchemyDbService:
    return SqlAlchemyDbService(session)


@router.post("/coil, response_model=CoilFromDb")
async def add_coil(coil: CoilAdd, db: SqlAlchemyDbService = Depends(get_db_service)):
    return await db.insert_coil(coil)


@router.delete("/coil")
async def delete_coil(coil: CoilDelete, db: SqlAlchemyDbService = Depends(get_db_service)):
    return await db.update_deletion_date(coil)


@router.get("/coil")
async def get_coil(start_date, end_date):
    return start_date, end_date


@router.get("/coil/stats")
async def get_coil_statistics(start_date, end_date, db: SqlAlchemyDbService = Depends(get_db_service)):
    return await db.get_statistic(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'))
