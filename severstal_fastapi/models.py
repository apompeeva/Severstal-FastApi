from sqlalchemy import MetaData, Integer, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import datetime

from database import Base


class Coil(Base):
    __tablename__ = "coil"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    creation_date: Mapped[datetime.date] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    deletion_date: Mapped[datetime.date] = mapped_column(TIMESTAMP)


