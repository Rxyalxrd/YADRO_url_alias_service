import random
import string

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.const import (
    SHORT_LINK_LEN,
    MAX_TRY_TO_GEN_SHORT_URL,
)
from app.dao import URLRepository


async def gen_short_path(
    session: AsyncSession,
    length=SHORT_LINK_LEN,
) -> str | None:
    """
    Генерирует уникальный короткий идентификатор для сокращённой ссылки.

    Args:
        url_repo (URLRepository): Репозиторий для взаимодействия с таблицей URL'ов.
        length (int, optional): Длина генерируемой строки. 
            По умолчанию берётся значение из константы GENERATE_SHORT_LINK.

    Raises:
        HTTPException: 500 - Внутренняя ошибка при проверке существования короткой ссылки.

    Returns:
        str: Уникальный короткий идентификатор для сокращённой ссылки.

    """

    logger.info("Начинаем генерировать short_path")

    count = 0

    while True:

        characters = string.ascii_letters + string.digits
        short_path = ''.join(random.sample(characters, length))

        try:
            exist = await URLRepository.get_by_short_url(short_path, session)

        except Exception:
            logger.critical("Ошибка проверки на существование короткой ссылки")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка проверки на существование короткой ссылки",
            )

        if not exist:
            logger.success("short_path создан")
            return short_path
        
        count += 1

        if count > MAX_TRY_TO_GEN_SHORT_URL:
            logger.warning("Превышено количество попыток генерации короткого url.")
            raise TimeoutError("Превышено количество попыток генерации короткого url.")
