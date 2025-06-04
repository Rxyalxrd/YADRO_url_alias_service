from typing import Sequence

from pydantic import HttpUrl
from sqlalchemy import (
    desc,
    exists,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
        url_obj: URLPair,
        session: AsyncSession,
    ) -> None:
        """
        Инкрементирует счётчики кликов за последний час и день для ссылки по её ID.

        Args:
            url_id (int): Идентификатор укороченной ссылки (URLPair).
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        """

        url_obj.stats.last_day_clicks += 1
        url_obj.stats.last_hour_clicks += 1

        session.add(url_obj)
        await session.commit()

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        is_activated: bool | None = None,
        limit: int = 10,
        offset: int = 0,
        sort_by_hour_clicks: bool = False,
        sort_by_day_clicks: bool = False,
    ) -> Sequence["URLPair"]:
        """
        Получает список ссылок с опциональной фильтрацией по статусу и сортировкой по кликам.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            is_activated (bool | None): Если указано, фильтрует по активности ссылки.
            limit (int): Максимальное количество ссылок для возврата.
            offset (int): Количество пропущенных записей (для пагинации).
            sort_by_hour_clicks (bool): Если True — сортировать по кликам за час (убывание).
            sort_by_day_clicks (bool): Если True — сортировать по кликам за день (убывание).

        Returns:
            Sequence[URLPair]: Список объектов URLPair, соответствующих условиям.

        """

        stmt = select(URLPair).options(joinedload(URLPair.stats))

        if is_activated is not None:
            stmt = stmt.where(URLPair.is_activated == is_activated)

        if sort_by_hour_clicks:
            stmt = stmt.join(URLPair.stats).order_by(desc(URLPairStat.last_hour_clicks))
        elif sort_by_day_clicks:
            stmt = stmt.join(URLPair.stats).order_by(desc(URLPairStat.last_day_clicks))

        stmt = stmt.limit(limit).offset(offset)

        result = await session.execute(stmt)

        return result.scalars().all()

        
    @classmethod
    async def deactivate_link(
        cls,
        short_code: str,
        session: AsyncSession,
    ) -> None:
        """
        Деактивирует укороченную ссылку (делает её недоступной для переходов) по коду.

        Args:
            short_code (str): Уникальный идентификатор укороченной ссылки (часть URL).
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        """

        stmt = (
            update(URLPair)
            .where(URLPair.short_url == short_code)
            .values(is_activated=False)
        )

        await session.execute(stmt)
        await session.commit()
