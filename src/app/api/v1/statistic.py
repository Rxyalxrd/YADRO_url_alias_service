from fastapi import (
    APIRouter,
    Depends,
)


router = APIRouter()


@router.get(
    "/created_short_url",
)
async def created_short_url():
    pass

@router.get(
    "/redirect_short_url",
)
async def redirect_short_url():
    pass