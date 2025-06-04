from fastapi import (
    HTTPException,
    status,
)
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import URLRepository
from app.models import URLPair


async def redirect(
    short_url: str,
    session: AsyncSession,
) -> URLPair:
    """
    Возвращает оригинальный URL по короткому идентификатору и увеличивает счётчик переходов.

    Args:
        short_url (str): Короткий идентификатор ссылки, по которому ищется оригинальный URL.
        session (AsyncSession): Асинхронная сессия SQLAlchemy для выполнения операций с БД.

    Returns:
        URLPair: Объект с оригинальной ссылкой и сопутствующей информацией.

    Raises:
        HTTPException: 404 - Если ссылка не найдена.
        HTTPException: 410 - Если ссылка неактивна или устарела.
        HTTPException: 500 - Внутренняя ошибка получения короткой ссылки.

    """

    logger.info("Начинаем переходить по ссылке")

    try:
        url = await URLRepository.get_by_short_url(short_url, session)

    except Exception:
        logger.critical("Ошибка получения короткой ссылки")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка получения короткой ссылки",
        )

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена"
        )

    if not url.is_activated:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ссылка неактивна"
        )

    if url.is_old:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ссылка устарела"
        )
    
    logger.info("Увеличиваем счетчик кликов")

    try:
        await URLRepository.increment_clicks(url, session)

    except Exception:
        logger.critical("Ошибка при увеличении кликов")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при увеличении кликов",
        )
    
    logger.success("Увеличили счетчик, переходим по ссылке...")
    
    return url
