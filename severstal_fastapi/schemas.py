from typing import Optional

from pydantic import BaseModel
from datetime import date


class CoilAdd(BaseModel):
    length: int
    weight: int


class Coil(CoilAdd):
    id: int
    creation_date: Optional[date]
    deletion_date: Optional[date]


class CoilFromBd(Coil):
    pass
