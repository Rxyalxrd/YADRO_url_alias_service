from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base


class ClickStat(Base):
    """
    Модель статистики кликов по укороченной ссылке.

    Attributes:
        id (int): Первичный ключ.
        last_hour_clicks (int): Кол-во кликов за последний час.
        last_day_clicks (int): Кол-во кликов за последние сутки.
        url (URL): Обратная связь на модель URL.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    last_hour_clicks: Mapped[int] = mapped_column(default=0)
    last_day_clicks: Mapped[int] = mapped_column(default=0)

    # Remove UniqueConstraint("url.id"), since URL.clickstats_id already is unique.

    # Relationship back to URL:
    url: Mapped["URL"] = relationship(
        uselist=False,
        back_populates="clickstats"
    )
