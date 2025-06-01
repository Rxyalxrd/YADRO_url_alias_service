from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import main_router 
from app.core import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
