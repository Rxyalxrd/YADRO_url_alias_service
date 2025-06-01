from sqlalchemy.orm import Mapped

from app.core import Base


class User(Base):
    """
    Модель пользователя для хранения учётных данных.

    Attributes:
        email (str): Уникальный адрес электронной почты пользователя.
        password (str): Хешированный пароль пользователя.

    """

    email: Mapped[str]
    password: Mapped[str]
