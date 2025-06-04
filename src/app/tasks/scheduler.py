from contextlib import asynccontextmanager
from datetime import (
    datetime,
    timezone,
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from loguru import logger
from sqlalchemy import update

from app.const import (
    DAILY_JOB,
    HOURLY_JOB,
)
from app.core import get_async_session
from app.models import (
    URLPair,
    URLPairStat,
)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


@asynccontextmanager
async def get_session():
    """
    Асинхронный контекстный менеджер для получения сессии SQLAlchemy.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.

    """

    async for session in get_async_session():
        yield session


async def deactivate_expired_urls():
    """
    Плановая задача для деактивации истёкших ссылок.

    Деактивирует все URL, у которых истёк срок действия (expires_at <= now)
    и которые всё ещё активны (is_activated=True). Также устанавливает is_old=True
    для дальнейшей фильтрации.

    """

    logger.info("Запущена задача деактивации ссылок")

    async with get_session() as session:
        now = datetime.now(timezone.utc)

        stmt = (
            update(URLPair)
            .where(URLPair.expires_at <= now, URLPair.is_activated)
            .values(is_activated=False, is_old=True)
        )

        result = await session.execute(stmt)
        await session.commit()

        logger.success(f"Деактивировано ссылок: {result.rowcount}")

async def reset_hourly_clicks():
    """
    Ежечасная задача: обнуляет поле `hourly_clicks` у всех записей.
    """
    logger.info("Запущена задача сброса hourly_clicks")

    async with get_session() as session:

        stmt = update(URLPairStat).values(last_hour_clicks=0)

        result = await session.execute(stmt)

        await session.commit()

        logger.success(f"Сброшено hourly_clicks у {result.rowcount} записей")


async def reset_daily_clicks():
    """
    Ежедневная задача: обнуляет поле `daily_clicks` у всех записей.
    """
    logger.info("Запущена задача сброса daily_clicks")

    async with get_session() as session:

        stmt = update(URLPairStat).values(last_day_clicks=0)

        result = await session.execute(stmt)

        await session.commit()

        logger.success(f"Сброшено daily_clicks у {result.rowcount} записей")


def start_scheduler():
    scheduler.add_job(
        deactivate_expired_urls,
        "interval",
        hours=DAILY_JOB,
        id="deactivate_expired_urls",
        replace_existing=True,
    )
    scheduler.add_job(
        reset_hourly_clicks,
        "interval",
        hours=HOURLY_JOB,
        id="reset_hourly_clicks",
        replace_existing=True,
    )
    scheduler.add_job(
        reset_daily_clicks,
        "interval",
        hours=DAILY_JOB,
        id="reset_daily_clicks",
        replace_existing=True,
    )
    scheduler.start()
