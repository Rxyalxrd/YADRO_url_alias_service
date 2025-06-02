from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import URLPair
from app.dao import URLRepository


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
        url_repo (URLRepository): Репозиторий доступа к данным таблицы ссылок.

    Returns:
        URL: Объект модели URL, добавленный в базу данных.

    Raises:
        ValueError: Если `short_url` уже существует в базе.

    """

    exist = await URLRepository.get_by_short_url(short_url, session)

    if exist:
        raise ValueError(f"Short URL '{short_url}' уже существует")

    ret = await URLRepository.add_url_pair(original_url, short_url, session)

    return ret