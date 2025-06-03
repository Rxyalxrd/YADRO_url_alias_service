from contextlib import asynccontextmanager
from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import update
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core import get_async_session
from app.models import URLPair
from app.const import DAILY_JOB


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


@asynccontextmanager
async def get_session():
    async for session in get_async_session():
        yield session


async def deactivate_expired_urls():
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


def start_scheduler():
    scheduler.add_job(
        deactivate_expired_urls,
        "interval",
        hours=DAILY_JOB,
        id="deactivate_expired_urls",
        replace_existing=True,
    )
    scheduler.start()
