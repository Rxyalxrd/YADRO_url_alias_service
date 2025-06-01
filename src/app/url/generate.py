import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.const import SHORT_LINK_LEN
from app.dao import URLRepository


async def gen_short_link(
    session: AsyncSession,
    length=SHORT_LINK_LEN,
) -> str | None:
    """
    Генерирует уникальный короткий идентификатор для сокращённой ссылки.

    Args:
        url_repo (URLRepository): Репозиторий для взаимодействия с таблицей URL'ов.
        length (int, optional): Длина генерируемой строки. 
            По умолчанию берётся значение из константы GENERATE_SHORT_LINK.

    Returns:
        str: Уникальный короткий идентификатор для сокращённой ссылки.

    """

    count = 0

    while True:


        characters = string.ascii_letters + string.digits
        gen_short_url = ''.join(
            random.choice(characters) for _, _ in enumerate(range(length))
        )

        exist = await URLRepository.get_by_short_url(gen_short_url, session)

        if not exist:
            return gen_short_url
        
        count += 1

        if count > 1000:
            logger.warning("Превышено количество попыток генерации короткого url.")
            break
        
    return None
