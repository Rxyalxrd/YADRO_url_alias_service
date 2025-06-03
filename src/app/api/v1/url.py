from fastapi import (
    APIRouter,
    Depends,
    Request,
    status,
)
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas import (
    URLRequest,
    URLResponse,
)
from app.models import User
from app.api.dependencies import get_current_user
from app.url import (
    gen_short_path,
    add_pair,
    deactivate_url,
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
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> URLResponse:
    """
    Создаёт короткую ссылку на основе переданного URL.

    Args:
        url (URLRequest): Входные данные, содержащие исходный URL.
        user (User): Текущий авторизованный пользователь (получен из токена).

    Returns:
        URLResponse: Короткая ссылка и связанный с ней оригинальный URL.

    """

    short_path = await gen_short_path(session)

    if not short_path:
        raise ValueError("Отсутствует short_url")

    urlpair = await add_pair(url.url, short_path, session)

    response = URLResponse.model_validate(urlpair).model_copy(
        update={"short_url": f"{request.base_url}{urlpair.short_url}"}
    )

    return response


@router.patch(
    "/deactivate/{short_url}",
    name="Деактивировать ссылку",
    summary="Деактивирует короткую ссылку",
    description="Устанавливает флаг `is_activated=False` для указанной сокращённой ссылки.",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def deactivate_short_url(
    short_url: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> Response:
    
    await deactivate_url(short_url, session)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
