from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import as_declarative, declared_attr

from app.core.settings import settings


@as_declarative()
class Base(AsyncAttrs):
    """
    Базовый класс для всех моделей SQLAlchemy.

    Этот класс используется как основа для определения моделей в SQLAlchemy.

    Methods
    -------
    __tablename__() -> str
        Генерация имени таблицы на основе имени класса.

    """

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
		Генерация имени таблицы на основе имени класса.

		Returns
		-------
		str
			Имя таблицы в нижнем регистре, соответствующее имени класса.

		"""

        return cls.__name__.lower()


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Генератор асинхронных сессий для работы с базой данных.

	Yields
	------
	AsyncSession
	    Экземпляр асинхронной сессии, используемый для взаимодействия с БД.

	"""

	async with AsyncSessionLocal() as async_session:
		yield async_session
