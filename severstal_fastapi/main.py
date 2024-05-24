from fastapi import FastAPI

from severstal_fastapi.endpoints import router

app = FastAPI()

app.include_router(router)