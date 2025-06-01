from fastapi.responses import RedirectResponse
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from app.dao import URLRepository
from app.api.dependencies import get_url_repository
from app.url import redirect


router = APIRouter()


@router.get(
    "/{short_url}",
    response_model=None,
    name="",
    summary="",
    description="",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def redirect_to_original(
    short_url: str,
    url_repo: URLRepository = Depends(get_url_repository),
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
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )
