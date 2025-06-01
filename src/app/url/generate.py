import random
import string

from app.const import GENERATE_SHORT_LINK
from app.dao import URLRepository


async def get_unique_short_id(
    url_repo: URLRepository,
    length=GENERATE_SHORT_LINK,
) -> str:
    """
    Генерирует уникальный короткий идентификатор для сокращённой ссылки.

    Args:
        url_repo (URLRepository): Репозиторий для взаимодействия с таблицей URL'ов.
        length (int, optional): Длина генерируемой строки. 
            По умолчанию берётся значение из константы GENERATE_SHORT_LINK.

    Returns:
        str: Уникальный короткий идентификатор для сокращённой ссылки.

    """

    while True:

        characters = string.ascii_letters + string.digits
        gen_short_url = ''.join(
            random.choice(characters) for _, _ in enumerate(range(length))
        )

        exist = await url_repo.short_url_exists(gen_short_url)

        if not exist:
            return gen_short_url
