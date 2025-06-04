from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core import get_async_session
from app.dao import URLRepository
from app.models import User
from app.schemas import URLResponse


router = APIRouter()


@router.get(
    "/all_crated_links",
    response_model=list[URLResponse],
    summary="Получить все созданные ссылки",
    description=(
        "Возвращает список всех URL-пар, которые были созданы сервисом. "
        "Поддерживается опциональная фильтрация по статусу активности и пагинация."
    ),
    name="Получить статистику"
)
async def all_crated_links(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    is_activated: bool | None = None,
    sort_by_hour_clicks: bool = False,
    sort_by_day_clicks: bool = False,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> Sequence[URLResponse]:
    """
    Возвращает список всех созданных коротких ссылок, привязанных к текущему пользователю.

    Args:
        request (Request): Объект запроса для получения базового URL (используется при формировании полного короткого URL).
        limit (int): Количество элементов на странице (по умолчанию 10).
        offset (int): Смещение от начала списка (по умолчанию 0).
        is_activated (bool | None): Фильтрация по статусу активности. Если None — фильтрация не применяется.
        sort_by_hour_clicks (bool): Сортировать по числу кликов за последний час (по убыванию), если True.
        sort_by_day_clicks (bool): Сортировать по числу кликов за последние сутки (по убыванию), если True.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для доступа к базе данных.
        user (User): Текущий авторизованный пользователь.

    Returns:
        Sequence[URLResponse]: Список сокращённых ссылок с актуальной статистикой и статусами.

    """
    
    ret = await URLRepository.get_all(
        session=session,
        is_activated=is_activated,
        limit=limit,
        offset=offset,
        sort_by_hour_clicks=sort_by_hour_clicks,
        sort_by_day_clicks=sort_by_day_clicks,
    )

    return [
        URLResponse.model_validate(item).model_copy(
            update={"short_url": f"{request.base_url}{item.short_url}"}
        )
        for item in ret
    ]
