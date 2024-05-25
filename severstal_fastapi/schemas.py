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


class CoilDelete(BaseModel):
    id: int


class CoilStats(BaseModel):
    added_count: int
    deleted_count: int
    avg_length: int
    avg_weight: int
    max_length: int
    min_length: int
    max_weight: int
    min_weight: int
    total_weight: int
    max_duration: int
    min_duration: int



