import datetime
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import Integer, select, func, and_, literal_column, or_
from sqlalchemy.ext.asyncio import AsyncSession

from severstal_fastapi.database import engine
from severstal_fastapi.models import Coil, Base
from severstal_fastapi.schemas import CoilAdd, CoilDelete, CoilStats, CoilFromBd


class Filter:
    def __init__(self, id_range_start: Optional[int] = None,
                 id_range_end: Optional[int] = None,
                 weight_range_start: Optional[int] = None,
                 weight_range_end: Optional[int] = None,
                 length_range_start: Optional[int] = None,
                 length_range_end: Optional[int] = None,
                 creation_date_range_start: Optional[datetime.date] = None,
                 creation_date_range_end: Optional[datetime.date] = None,
                 deletion_date_range_start: Optional[datetime.date] = None,
                 deletion_date_range_end: Optional[datetime.date] = None):
        self.id_range_start = id_range_start
        self.id_range_end = id_range_end
        self.weight_range_start = weight_range_start
        self.weight_range_end = weight_range_end
        self.length_range_start = length_range_start
        self.length_range_end = length_range_end
        self.creation_date_range_start = creation_date_range_start
        self.creation_date_range_end = creation_date_range_end
        self.deletion_date_range_start = deletion_date_range_start
        self.deletion_date_range_end = deletion_date_range_end

    def get_conditions(self, query):
        filters = [
            ((Coil.id >= self.id_range_start) if self.id_range_start else True),
            ((Coil.id <= self.id_range_end) if self.id_range_end else True),
            ((Coil.weight >= self.weight_range_start) if self.weight_range_start else True),
            ((Coil.weight <= self.weight_range_end) if self.weight_range_end else True),
            ((Coil.length >= self.length_range_start) if self.length_range_start else True),
            ((Coil.length <= self.length_range_end) if self.length_range_end else True),
            ((Coil.creation_date >= self.creation_date_range_start) if self.creation_date_range_start else True),
            ((Coil.creation_date <= self.creation_date_range_end) if self.creation_date_range_end else True),
            ((Coil.deletion_date >= self.deletion_date_range_start) if self.deletion_date_range_start else True),
            ((Coil.deletion_date <= self.deletion_date_range_end) if self.deletion_date_range_end else True),
        ]
        for statement in filters:
            query = query.where(statement)

        return query


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
        try:
            if cur_coil.deletion_date is None:
                cur_coil.deletion_date = datetime.date.today()
                await self.session.commit()
                return cur_coil
        except AttributeError:
            return "Coil with this id was not found"

    async def get_coil(self, filter: Filter):
        query = (select(Coil.id, Coil.length, Coil.weight, Coil.creation_date, Coil.deletion_date)
                 .select_from(Coil))
        query = filter.get_conditions(query)
        res = await self.session.execute(query)
        result = res.fetchall()
        print(result)
        result_dto = [CoilFromBd.model_validate(row, from_attributes=True) for row in result]
        return result_dto

    async def get_statistic(self, start_date: datetime.date, end_date: datetime.date):
        added_coils_cte = (
            select(func.count().label("added_count"))
                .select_from(Coil)
                .filter(and_(Coil.creation_date >= start_date), (Coil.creation_date <= end_date))
                .cte("added_coil")
        )

        deleted_coils_cte = (
            select(func.count().label("deleted_count"))
                .select_from(Coil)
                .filter(and_(Coil.deletion_date >= start_date), (Coil.deletion_date <= end_date))
                .cte("deleted_coil")
        )

        coils_in_storage_cte = (
            select(Coil.id, Coil.length, Coil.weight, Coil.creation_date, Coil.deletion_date)
                .select_from(Coil)
                .where(or_((Coil.creation_date <= end_date), (Coil.deletion_date > start_date)))
                .cte("coil_storage")
        )

        summary_cte = select(
            func.avg(coils_in_storage_cte.c.length).cast(Integer).label("avg_length"),
            func.avg(coils_in_storage_cte.c.weight).cast(Integer).label("avg_weight"),
            func.max(coils_in_storage_cte.c.length).label("max_length"),
            func.min(coils_in_storage_cte.c.length).label("min_length"),
            func.max(coils_in_storage_cte.c.weight).label("max_weight"),
            func.min(coils_in_storage_cte.c.weight).label("min_weight"),
            func.sum(coils_in_storage_cte.c.weight).label("total_weight"),
            func.max(coils_in_storage_cte.c.deletion_date - coils_in_storage_cte.c.creation_date).label("max_duration"),
            func.min(coils_in_storage_cte.c.deletion_date - coils_in_storage_cte.c.creation_date).label("min_duration")
        ).select_from(coils_in_storage_cte).cte("summary")

        main_query = select(
            added_coils_cte.c.added_count,
            deleted_coils_cte.c.deleted_count,
            summary_cte.c.avg_length,
            summary_cte.c.avg_weight,
            summary_cte.c.max_length,
            summary_cte.c.min_length,
            summary_cte.c.max_weight,
            summary_cte.c.min_weight,
            summary_cte.c.total_weight,
            summary_cte.c.max_duration,
            summary_cte.c.min_duration
        ).select_from(
            added_coils_cte.join(
                deleted_coils_cte,
                literal_column("1=1")
            ).join(
                summary_cte,
                literal_column("1=1")
            )
        )
        res = await self.session.execute(main_query)
        result = res.fetchall()
        print(result)
        result_dto = [CoilStats.model_validate(row, from_attributes=True) for row in result]
        return result_dto
