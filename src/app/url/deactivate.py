from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import URLRepository

async def deactivate_url(
    short_url: str,
    session: AsyncSession,
) -> None:
    
    short_code = urlparse(short_url).path.lstrip("/")

    await URLRepository.deactivate_link(short_code, session)
