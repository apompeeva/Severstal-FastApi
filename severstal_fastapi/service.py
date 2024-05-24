from sqlalchemy.ext.asyncio import AsyncSession

from severstal_fastapi.database import engine, async_session_maker
from severstal_fastapi.models import Coil, Base
from severstal_fastapi.schemas import CoilAdd


class AsyncORM:
    def __init__(self, session: AsyncSession):  # при инициализации принимает асинхронную сессию
        self.session = session

    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def insert_coil(self, coil: CoilAdd):
        new_coil = Coil(**coil.model_dump())
        self.session.add(new_coil)
        # flush взаимодействует с БД, поэтому пишем await
        await self.session.flush()
        await self.session.commit()
        return new_coil


