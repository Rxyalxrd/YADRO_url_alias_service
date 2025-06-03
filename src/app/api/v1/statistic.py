from enum import Enum
from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import URLResponse
from app.core import get_async_session
from app.dao import URLRepository
from app.api.dependencies import get_current_user


router = APIRouter()


class Period(str, Enum):
    hour = "hour"
    day = "day"

@router.get(
    "/all_crated_links",
    response_model=list[URLResponse],
    summary="Получить все созданные ссылки",
    description=(
        "Возвращает список всех URL-пар, которые были созданы сервисом. "
        "Поддерживается опциональная фильтрация по статусу активности и пагинация."
    ),
)
async def all_crated_links(
    request: Request,
    is_activated: bool = True,
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> Sequence[URLResponse]:
    
    ret = await URLRepository.get_all(
        session=session,
        is_activated=is_activated,
        limit=limit,
        offset=offset,
    )

    return [
        URLResponse.model_validate(item).model_copy(
            update={"short_url": f"{request.base_url}{item.short_url}"}
        )
        for item in ret
    ]
