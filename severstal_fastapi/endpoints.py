from datetime import datetime, date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from severstal_fastapi.database import get_async_session
from severstal_fastapi.service import SqlAlchemyDbService, Filter
from severstal_fastapi.schemas import CoilAdd, CoilDelete

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
async def get_coils(id_range_start: Optional[int] = None,
                    id_range_end: Optional[int] = None,
                    weight_range_start: Optional[int] = None,
                    weight_range_end: Optional[int] = None,
                    length_range_start: Optional[int] = None,
                    length_range_end: Optional[int] = None,
                    creation_date_range_start: Optional[date] = None,
                    creation_date_range_end: Optional[date] = None,
                    deletion_date_range_start: Optional[date] = None,
                    deletion_date_range_end: Optional[date] = None,
                    db: SqlAlchemyDbService = Depends(get_db_service)):
    filter = Filter(id_range_start,
                    id_range_end,
                    weight_range_start,
                    weight_range_end,
                    length_range_start,
                    length_range_end,
                    creation_date_range_start,
                    creation_date_range_end,
                    deletion_date_range_start,
                    deletion_date_range_end)
    return await db.get_coil(filter)


@router.get("/coil/stats")
async def get_coil_statistics(start_date, end_date, db: SqlAlchemyDbService = Depends(get_db_service)):
    return await db.get_statistic(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d'))
