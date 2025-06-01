from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import RedirectResponse

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
    redirect,
)


router = APIRouter()


@router.post(
    "/cut_url",
    response_model=None,
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

@router.get(
    "/deactivate",
    response_model=None,
    name="",
    summary="",
    description="",
)
async def deactivate_short_url():
    pass

@router.get(
    "/{short_url}",
    response_model=None,
    name="",
    summary="",
    description="",
    status_code=status.HTTP_303_SEE_OTHER
)
async def redirect_to_original(
    short_url: str,
    url_repo: URLRepository = Depends(get_url_repository),
    user: User = Depends(get_current_user),
) -> RedirectResponse:
    """
    Перенаправляет пользователя с короткой ссылки на оригинальный URL.

    Args:
        short_url (str): Уникальный код короткой ссылки, например "Y8mMtv".
        url_repo (URLRepository): Репозиторий URL для получения оригинальной ссылки.

    Returns:
        RedirectResponse: HTTP 307 перенаправление на оригинальный URL.

    """

    url = await redirect(short_url, url_repo)
    
    return RedirectResponse(
        url.original_url,
        status_code=status.HTTP_303_SEE_OTHER
    )
