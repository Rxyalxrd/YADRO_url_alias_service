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

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.

        """

        self.session = session

    async def short_url_exists(self, short_url: str) -> bool:
        """
        Проверяет, существует ли уже запись с данным short_url.
        Используется для предотвращения коллизий при генерации коротких ссылок.

        Args:
            short_url (str): Генерируемая короткая ссылка.

        Returns:
            bool: True, если short_url уже существует, иначе False.

        """

        stmt = select(exists().where(URL.short_url == short_url))

        ret = await self.session.execute(stmt)

        return ret.scalar_one()

    async def get_by_short_url(self, short_url: str) -> URL | None:
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

        ret = await self.session.execute(stmt)

        return ret.scalar_one_or_none()
    
    async def add_url_pair(
        self,
        original_url: HttpUrl,
        short_url: str,
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

        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url
