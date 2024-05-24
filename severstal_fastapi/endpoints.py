from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from severstal_fastapi.database import get_async_session
from severstal_fastapi.service import AsyncORM
from severstal_fastapi.schemas import CoilAdd

router = APIRouter()


async def get_todo_repository(session: AsyncSession = Depends(get_async_session)) -> AsyncORM:
    return AsyncORM(session)


@router.post("/coil, response_model=CoilFromDb")
async def add_coil(coil: CoilAdd, repo: AsyncORM = Depends(get_todo_repository)):
    return await repo.insert_coil(coil)


@router.delete("/coil")
async def delete_coil():
    pass


@router.get("/coil")
async def get_coil():
    pass


@router.get("/coil/stats")
async def get_coil_statistics():
    pass
