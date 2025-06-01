from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from app.core import Base

if TYPE_CHECKING:
    from .statistics import ClickStat


class URL(Base):
    """
    Модель укороченной ссылки.

    Attributes:
        id (int): Первичный ключ.
        short_url (str): Уникальный сокращённый идентификатор ссылки.
        original_url (str): Оригинальный (длинный) URL.
        is_activated (bool): Флаг активности ссылки (может ли она перенаправлять).
        is_old (bool): Флаг старой ссылки (для автоудаления или архивирования).
        clickstats (ClickStat): Статистика кликов по данной ссылке.

    """

    id: Mapped[int] = mapped_column(primary_key=True)
    short_url: Mapped[str] = mapped_column(unique=True, index=True)
    original_url: Mapped[str] = mapped_column()
    is_activated: Mapped[bool]
    is_old: Mapped[bool]
    clickstats: Mapped["ClickStat"] = relationship(
        back_populates="url",
        uselist=False,
        cascade="all, delete-orphan",
    )
