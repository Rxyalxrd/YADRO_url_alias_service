from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import URLRepository
from app.models import URLPair

async def redirect(
    short_url: str,
    session: AsyncSession,
) -> URLPair:

    url = await URLRepository.get_by_short_url(short_url, session)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена"
        )

    if not url.is_activated:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ссылка неактивна"
        )

    if url.is_old:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Ссылка устарела"
        )
    
    await URLRepository.increment_clicks(url.id, session)
    
    return url
