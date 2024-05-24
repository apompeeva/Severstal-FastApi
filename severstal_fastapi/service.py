import datetime
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from severstal_fastapi.database import engine, async_session_maker
from severstal_fastapi.models import Coil, Base
from severstal_fastapi.schemas import CoilAdd, CoilDelete


class DbService(ABC):

    @staticmethod
    @abstractmethod
    async def create_tables():
        pass

    @abstractmethod
    async def insert_coil(self) -> Coil:
        pass


class SqlAlchemyDbService(DbService):
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
        await self.session.flush()
        await self.session.commit()
        return new_coil

    async def update_deletion_date(self, coil: CoilDelete):
        cur_coil = await self.session.get(Coil, coil.id)
        if cur_coil.deletion_date is None:
            cur_coil.deletion_date = datetime.datetime.utcnow()
            await self.session.commit()
        return cur_coil



