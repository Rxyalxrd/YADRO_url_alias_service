from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas import (
    URLRequest,
    URLResponse,
)
from app.models import (
    User,
    URL,
)
from app.api.dependencies import (
    get_current_user,
)
from app.url import (
    gen_short_link,
    add_pair,
)


router = APIRouter()


@router.post(
    "/cut_url",
    response_model=URLResponse,
    name="Cut url",
    summary="Создание короткой ссылки",
    description=(
        "Генерирует уникальную короткую ссылку для переданного URL. "
        "URL будет сохранён в базе данных и привязан к текущему пользователю. "
        "Возвращает сгенерированную короткую ссылку и исходный URL."
    ),
)
async def cut_url(
    url: URLRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> URL:
    """
    Создаёт короткую ссылку на основе переданного URL.

    Args:
        url (URLRequest): Входные данные, содержащие исходный URL.
        url_repo (URLRepository): Репозиторий URL-ов (через Depends).
        user (User): Текущий авторизованный пользователь (получен из токена).

    Returns:
        URLResponse: Короткая ссылка и связанный с ней оригинальный URL.

    """

    short_url = await gen_short_link(session)

    if not short_url:
        raise ValueError("Отссутсвует short_url")

    ret = await add_pair(url.url, short_url, session)

    return ret

@router.get(
    "/deactivate",
    response_model=None,
    name="",
    summary="",
    description="",
)
async def deactivate_short_url():
    pass

