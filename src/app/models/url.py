from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base
from app.models.statistics import ClickStat


class URL(Base):
    """
    Модель укороченной ссылки.

    Attributes:
        short_url (str): Уникальный сокращённый идентификатор ссылки.
        original_url (str): Оригинальный (длинный) URL.
        is_activated (bool): Флаг активности ссылки (может ли она перенаправлять).
        is_old (bool): Флаг старой ссылки (для автоудаления или архивирования).
        clickstats (ClickStat): Статистика кликов по данной ссылке (one-to-one).
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    short_url: Mapped[str] = mapped_column(unique=True)
    original_url: Mapped[str]
    is_activated: Mapped[bool]
    is_old: Mapped[bool]

    # Foreign key referencing ClickStat.id; unique enforces one-to-one
    clickstats_id: Mapped[int] = mapped_column(
        ForeignKey("clickstat.id"), unique=True
    )

    # Relationship: each URL has exactly one ClickStat
    clickstats: Mapped["ClickStat"] = relationship(
        uselist=False,
        cascade="all, delete-orphan",
        back_populates="url",
    )
