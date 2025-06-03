from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import main_router 
from app.core import settings
from app.tasks import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

app.include_router(main_router)
