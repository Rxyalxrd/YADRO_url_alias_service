from .auth import router as auth_router
from .url import router as url_router
from .statistic import router as statistic_router
from .redirect import router as redirect_router

__all__ = (
    "auth_router",
    "url_router",
    "statistic_router",
    "redirect_router",
)
