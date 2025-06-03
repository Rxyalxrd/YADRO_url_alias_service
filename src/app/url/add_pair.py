from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import HttpUrl

from app.dao import URLRepository
from app.models import URLPair
from loguru import logger


async def add_pair(
    original_url: HttpUrl,
    short_url: str,
    session: AsyncSession,
) -> URLPair:
    """
    Добавляет новую пару короткой и оригинальной ссылок в базу данных.

    Args:
        original_url (HttpUrl): Исходная (полная) URL-ссылка, которую нужно сократить.
        short_url (str): Сгенерированная короткая ссылка (идентификатор).
        session (AsyncSession): Сессия для работы с БД.

    Returns:
        URLPair: Объект модели URL, добавленный в базу данных.

    Raises:
        HTTPException: 409 - Если короткая ссылка уже существует.
        HTTPException: 500 - При внутренней ошибке базы данных.

    """

    logger.info("Добавляем новую пару")

    try:
        exist = await URLRepository.get_by_short_url(short_url, session)

    except Exception:
        logger.critical("Ошибка проверки на существование короткой ссылки")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка проверки на существование короткой ссылки",
        )

    if exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL '{short_url}' уже существует",
        )

    try:
        ret = await URLRepository.add_url_pair(original_url, short_url, session)

    except Exception:
        logger.critical("Ошибка при добавлении пары")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при добавлении ссылки",
        )

    logger.success("Добавлена новая пара")

    return ret
