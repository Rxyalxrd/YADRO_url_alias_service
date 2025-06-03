from urllib.parse import urlparse

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.dao import URLRepository


async def deactivate_url(
    short_url: str,
    session: AsyncSession,
) -> None:
    
    """
    Деактивирует короткую ссылку, делая её недоступной для перехода.

    Args:
        short_url (str): Полная короткая ссылка, из которой извлекается короткий код
            (например, "https://short.ly/Y8mMtv" → "Y8mMtv").
        session (AsyncSession): Асинхронная сессия SQLAlchemy для доступа к базе данных.

    Raises:
        HTTPException: 400 - Если не передана ссылка или не верно указана.
        HTTPException: 404 - Если ссылка не найдена.

    """

    logger.info("Начинаем деактивировать короткую ссылку")
    
    short_code = urlparse(short_url).path.lstrip("/")

    if not short_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверная короткая ссылка"
        )
    
    exist = await URLRepository.short_url_exists(short_code, session)

    if not exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена",
        )

    await URLRepository.deactivate_link(short_code, session)

    logger.success("Ссылка деактивирована")
