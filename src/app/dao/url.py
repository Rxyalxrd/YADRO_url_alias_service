from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    exists,
)

from app.models import (
    URL,
    ClickStat,
)


class URLRepository:
    """
    Репозиторий для работы с моделью URL и статистикой ClickStat.

    Обеспечивает методы для проверки уникальности, получения по short_url
    и добавления новых записей.

    """

    @classmethod
    async def short_url_exists(cls, short_url: str, session: AsyncSession) -> bool:
        """
        Проверяет, существует ли уже запись с данным short_url.
        Используется для предотвращения коллизий при генерации коротких ссылок.

        Args:
            short_url (str): Генерируемая короткая ссылка.

        Returns:
            bool: True, если short_url уже существует, иначе False.

        """

        stmt = select(exists().where(URL.short_url == short_url))

        ret = await session.execute(stmt)

        return ret.scalar_one()

    @classmethod
    async def get_by_short_url(
        cls,
        short_url: str,
        session: AsyncSession
    ) -> URL | None:
        """
        Получить объект URL по его короткой ссылке.

        Args:
            short_url (str): Короткий URL.

        Returns:
            URL | None: Найденный объект или None, если не найден.

        """

        stmt = (
            select(URL)
            .where(URL.short_url == short_url)
            .limit(1)
        )

        ret = await session.execute(stmt)

        return ret.scalar_one_or_none()
    
    @classmethod
    async def add_url_pair(
        cls,
        original_url: HttpUrl,
        short_url: str,
        session: AsyncSession,
        is_activated: bool = True,
        is_old: bool = False, 
    ) -> URL:
        """
        Добавляет новую пару original_url и short_url в базу данных.
        Также создаёт связанный ClickStat.

        Args:
            original_url (HttpUrl): Полная оригинальная ссылка.
            short_url (str): Сгенерированная короткая ссылка.
            is_activated (bool): Активна ли ссылка.
            is_old (bool): Устаревшая ли ссылка.

        Returns:
            URL: Сохранённая модель URL.

        """

        url = URL(
            original_url=str(original_url),
            short_url=short_url,
            is_activated=is_activated,
            is_old=is_old,
        )

        url.clickstats = ClickStat(
            last_hour_clicks=0,
            last_day_clicks=0,
        )

        session.add(url)
        await session.commit()
        await session.refresh(url)

        return url
