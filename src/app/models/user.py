import datetime as dt

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core import Base


class User(Base):
    """
    Модель пользователя для хранения учётных данных.

    Attributes:
        email (str): Уникальный адрес электронной почты пользователя.
        password (str): Хешированный пароль пользователя.

    """

    email: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]
    created_at: Mapped[dt.datetime] = mapped_column(index=True, server_default=func.now())
