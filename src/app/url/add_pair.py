from pydantic import HttpUrl

from app.dao import URLRepository
from app.models import URL


async def add_pair(
    original_url: HttpUrl,
    short_url: str,
    url_repo: URLRepository,
) -> URL:
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

    exist = await url_repo.short_url_exists(short_url)

    if exist:
        raise ValueError(f"Short URL '{short_url}' уже существует")

    ret = await url_repo.add_url_pair(original_url, short_url)

    return ret