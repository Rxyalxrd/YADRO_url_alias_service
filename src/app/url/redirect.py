from fastapi import (
    HTTPException,
    status,
)

from app.dao import URLRepository


async def redirect(short_url: str, url_repo: URLRepository):

    url = await url_repo.get_by_short_url(short_url)
    
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
    
    return url
