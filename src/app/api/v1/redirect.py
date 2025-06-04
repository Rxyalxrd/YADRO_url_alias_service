from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.services import redirect

router = APIRouter()


@router.get(
    "/{short_url}",
    include_in_schema=False,
    status_code=status.HTTP_303_SEE_OTHER,
    name="Перейти по короткой ссылке",
    summary="Перенаправление по короткой ссылке",
    description=(
        "Обрабатывает переход по короткой ссылке. "
        "По коду ссылки (например, `Y8mMtv`) находит соответствующий оригинальный URL "
        "в базе данных и выполняет перенаправление с кодом 303 (See Other) "
        "на этот URL. Если ссылка недействительна или отключена, будет выброшено исключение."
    ),
)
async def redirect_to_original(
    short_url: str,
    session: AsyncSession = Depends(get_async_session),
) -> RedirectResponse:
    """
    Перенаправляет пользователя с короткой ссылки на оригинальный URL.

    Args:
        short_url (str): Уникальный код короткой ссылки, например "Y8mMtv".
        url_repo (URLRepository): Репозиторий URL для получения оригинальной ссылки.

    Returns:
        RedirectResponse: HTTP 303 перенаправление на оригинальный URL.

    """

    url = await redirect(short_url, session)

    return RedirectResponse(
        await url.awaitable_attrs.original_url,
        status_code=status.HTTP_303_SEE_OTHER,
    )
