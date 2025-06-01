from fastapi import (
    APIRouter,
    Depends,
)

from app.schemas import (
    URLRequest,
    URLResponse,
)
from app.models import User
from app.dao import URLRepository
from app.api.dependencies import (
    get_current_user,
    get_url_repository,
)
from app.url import (
    get_unique_short_id,
    add_pair,
)


router = APIRouter()


@router.post(
    "/cut_url",
    response_model=None,
    summary="Создание короткой ссылки",
    description=(
        "Генерирует уникальную короткую ссылку для переданного URL. "
        "URL будет сохранён в базе данных и привязан к текущему пользователю. "
        "Возвращает сгенерированную короткую ссылку и исходный URL."
    ),
)
async def cut_url(
    url: URLRequest,
    url_repo: URLRepository = Depends(get_url_repository),
    user: User = Depends(get_current_user),
) -> URLResponse:
    """
    Создаёт короткую ссылку на основе переданного URL.

    Args:
        url (URLRequest): Входные данные, содержащие исходный URL.
        url_repo (URLRepository): Репозиторий URL-ов (через Depends).
        user (User): Текущий авторизованный пользователь (получен из токена).

    Returns:
        URLResponse: Короткая ссылка и связанный с ней оригинальный URL.

    """

    short_url = await get_unique_short_id(url_repo)

    ret = await add_pair(url.url, short_url, url_repo)

    return ret