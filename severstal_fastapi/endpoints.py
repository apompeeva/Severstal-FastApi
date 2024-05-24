from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from severstal_fastapi.database import get_async_session
from severstal_fastapi.service import DbService
from severstal_fastapi.schemas import CoilAdd, CoilDelete

router = APIRouter()


async def get_db_service(session: AsyncSession = Depends(get_async_session)) -> DbService:
    return DbService(session)


@router.post("/coil, response_model=CoilFromDb")
async def add_coil(coil: CoilAdd, db: DbService = Depends(get_db_service)):
    return await db.insert_coil(coil)


@router.delete("/coil")
async def delete_coil(coil: CoilDelete, db: DbService = Depends(get_db_service)):
    return await db.update_deletion_date(coil)


@router.get("/coil")
async def get_coil():
    pass


@router.get("/coil/stats")
async def get_coil_statistics():
    pass
