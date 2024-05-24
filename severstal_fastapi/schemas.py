from typing import Optional

from pydantic import BaseModel
from datetime import date


class CoilCreate(BaseModel):
    length: int
    weight: int


class Coil(CoilCreate):
    id: int
    creation_date: date
    deletion_date: Optional[date]
