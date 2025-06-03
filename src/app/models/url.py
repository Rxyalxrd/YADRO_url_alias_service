import datetime as dt

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base


class URLPair(Base):
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
    short_url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    original_url: Mapped[str] = mapped_column(nullable=False)
    is_activated: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_old: Mapped[bool] = mapped_column(default=False, nullable=False)
    expires_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=30), # days=1
        nullable=False,
    )

    stats: Mapped["URLPairStat"] = relationship(
        back_populates="url",
        uselist=False,
        cascade="all",
        lazy="subquery",
    )


class URLPairStat(Base):
    """
    Модель статистики кликов по укороченной ссылке.

    Attributes:
        id (int): Первичный ключ.
        last_hour_clicks (int): Кол-во кликов за последний час.
        last_day_clicks (int): Кол-во кликов за последние сутки.
        url (URL): Обратная связь на модель URL.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(
        ForeignKey("urlpair.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    last_hour_clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    last_day_clicks: Mapped[int] = mapped_column(default=0, nullable=False)

    url: Mapped["URLPair"] = relationship(
        back_populates="stats",
        uselist=False,
        lazy="subquery",
    )
