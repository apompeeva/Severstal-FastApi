import datetime
from abc import ABC, abstractmethod

from sqlalchemy import Integer, select, func, cte, and_, literal_column, or_
from sqlalchemy.ext.asyncio import AsyncSession

from severstal_fastapi.database import engine, async_session_maker
from severstal_fastapi.models import Coil, Base
from severstal_fastapi.schemas import CoilAdd, CoilDelete, StatsRange, CoilStats


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

    async def get_statistic(self, start_date: datetime.date, end_date: datetime.date):
        '''
        WITH AddedCoils AS (
                    SELECT COUNT( * ) AS added_count
                    FROM coil
                    WHERE creation_date >= 'start_date' AND creation_date <= 'end_date'
        ),
        DeletedCoils AS (
                    SELECT COUNT( * ) AS deleted_count
                    FROM coil
                    WHERE deletion_date >= 'start_date' AND deletion_date <= 'end_date'
        ),
        CoilsInStorage AS (
                    SELECT id, length, weight
                    FROM coil
                    WHERE creation_date <= 'end_date' or deletion_date > 'start_date'
        ),
        Summary AS (
                    SELECT AVG(length) AS avg_length,
                           AVG(weight) AS avg_weight,
                            MAX(length) AS max_length,
                            MIN(length) AS min_length,
                            MAX(weight) AS max_weight,
                            MIN(weight) AS min_weight,
                            SUM(weight) AS total_weight
                    FROM CoilsInStorage
                    )
        SELECT a.added_count, d.deleted_count, s.avg_length, s.avg_weight, s.max_length, s.min_length, s.max_weight, s.min_weight, s.total_weight,
                (SELECT MAX(deletion_date - creation_date) FROM coil WHERE creation_date >= 'start_date' AND deletion_date <= 'end_date') AS max_duration,
                (SELECT MIN(deletion_date - creation_date) FROM coil WHERE creation_date >= 'start_date' AND deletion_date <= 'end_date') AS min_duration
        FROM AddedCoils a
        JOIN DeletedCoils d ON 1 = 1 -- Join for consistency of dates
        JOIN Summary s ON 1 = 1 -- Join for summary stats
        ORDER BY a.added_count, d.deleted_count;
        '''
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
            func.max(func.date_part('day', coils_in_storage_cte.c.deletion_date -
                                    coils_in_storage_cte.c.creation_date)).label("max_duration"),
            func.min(func.date_part('day', coils_in_storage_cte.c.deletion_date -
                                    coils_in_storage_cte.c.creation_date)).label("min_duration")
        ).select_from(coils_in_storage_cte).cte("summary")

        # Define the main query
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
        print(main_query.compile(dialect=engine.dialect))
        res = await self.session.execute(main_query)
        result = res.fetchall()
        print(result)
        result_dto = [CoilStats.model_validate(row, from_attributes=True) for row in result]
        return result_dto




