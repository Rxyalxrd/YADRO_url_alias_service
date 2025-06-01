from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
	AsyncSession,
	create_async_engine,
	async_sessionmaker,
)
from sqlalchemy.orm import (
    declared_attr,
    declarative_base,
    Mapped,
    mapped_column,
)

from .settings import settings


class PreBase:
    """
    Базовый класс для всех моделей SQLAlchemy.

    Этот класс используется как основа для определения моделей в SQLAlchemy.
    Он автоматически генерирует имя таблицы и первичный ключ.

    Attributes
    ----------
    id : id
        Внешний ключ для таблицы.

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

        Parameters
        ----------
        None    

		Returns
		-------
		str
			Имя таблицы в нижнем регистре, соответствующее имени класса.

		"""

        return cls.__name__.lower()

    id: Mapped[int] =  mapped_column(primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(bind=engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Генератор асинхронных сессий для работы с базой данных.

	Parameters
	----------
	None

	Yields
	------
	AsyncSession
	    Экземпляр асинхронной сессии, используемый для взаимодействия с БД.

	"""

	async with AsyncSessionLocal() as async_session:
		yield async_session
