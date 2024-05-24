from fastapi import APIRouter

from schemas import CoilCreate

router = APIRouter()


@router.post("/coil")
async def add_coil(coil: CoilCreate):
    return


@router.delete("/coil")
async def delete_coil():
    pass


@router.get("/coil")
async def get_coil():
    pass


@router.get("/coil/stats")
async def get_coil_statistics():
    pass
