from typing import Sequence

from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    exists,
    update,
)

from app.models import (
    URLPair,
    URLPairStat,
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

        stmt = select(exists().where(URLPair.short_url == short_url))

        ret = await session.execute(stmt)

        return ret.scalar_one()

    @classmethod
    async def get_by_short_url(
        cls,
        short_url: str,
        session: AsyncSession
    ) -> URLPair | None:
        """
        Получить объект URL по его короткой ссылке.

        Args:
            short_url (str): Короткий URL.

        Returns:
            URL | None: Найденный объект или None, если не найден.

        """

        stmt = (
            select(URLPair)
            .where(URLPair.short_url == short_url)
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
    ) -> URLPair:
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

        urlstat = URLPairStat(
            last_hour_clicks=0,
            last_day_clicks=0,
        ) # type: ignore

        url = URLPair(
            original_url=str(original_url),
            short_url=short_url,
            is_activated=is_activated,
            is_old=is_old,
            stats=urlstat,
        ) # type: ignore

        session.add(url)
        await session.commit()
        await session.refresh(url)

        return url

    @classmethod
    async def increment_clicks(
        cls,
        url_id: int,
        session: AsyncSession,
    ) -> None:
        """
        Увеличивает поля last_hour_clicks и last_day_clicks на 1 для записи URLPair с данным id.
        """

        stmt = (
            update(URLPairStat)
            .where(URLPairStat.url_id == url_id)
            .values(
                last_hour_clicks=URLPairStat.last_hour_clicks + 1,
                last_day_clicks=URLPairStat.last_day_clicks + 1,
            )
        )

        await session.execute(stmt)
        await session.commit()

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        is_activated: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Sequence["URLPair"]:

        stmt = select(URLPair)

        if is_activated is not None:
            stmt = stmt.where(URLPair.is_activated == is_activated)

        stmt = stmt.limit(limit).offset(offset)

        ret = await session.execute(stmt)

        return ret.scalars().all()
    
    @classmethod
    async def deactivate_link(
        cls,
        short_code: str,
        session: AsyncSession,
    ) -> None:
        
        stmt = (
            update(URLPair)
            .where(URLPair.short_url == short_code)
            .values(is_activated=False)
        )

        await session.execute(stmt)
        await session.commit()
