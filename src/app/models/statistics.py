from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import ForeignKey

from app.core import Base

if TYPE_CHECKING:
    from .url import URL


class ClickStat(Base):
    """
    Модель статистики кликов по укороченной ссылке.

    Attributes:
        link_id (int): Внешний ключ на URL.id, уникален (OneToOne).
        last_hour_clicks (int): Кол-во кликов за последний час.
        last_day_clicks (int): Кол-во кликов за последние сутки.
        url (URL): Обратная связь на модель URL.

    """

    link_id: Mapped[int] = mapped_column(ForeignKey("url.id", ondelete="CASCADE"), unique=True)
    last_hour_clicks: Mapped[int] = mapped_column(default=0)
    last_day_clicks: Mapped[int] = mapped_column(default=0)
    url: Mapped["URL"] = relationship(back_populates="clickstats")
