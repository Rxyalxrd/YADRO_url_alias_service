from fastapi import APIRouter

from app.api.v1 import (
    auth_router,
    redirect_router,
    statistic_router,
    url_router,
)


main_router = APIRouter()

main_router.include_router(
    auth_router,
    prefix="/auth/jwt",
    tags=["Auth"],
)
main_router.include_router(
    url_router,
    prefix="/api/v1",
    tags=["Url aliases"],
)
main_router.include_router(
    statistic_router,
    prefix="/api/v1",
    tags=["Monitoring"],
)
main_router.include_router(
    redirect_router,
    prefix="",
    tags=["Redirect"],
)
