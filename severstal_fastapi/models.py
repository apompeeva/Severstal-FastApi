from typing import Optional

from sqlalchemy import MetaData, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import datetime



metadata = MetaData()


class Base(DeclarativeBase):
    pass


class Coil(Base):
    __tablename__ = "coil"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    creation_date: Mapped[Optional[datetime.date]] = mapped_column(default=datetime.date.today)
    deletion_date: Mapped[Optional[datetime.date]]


