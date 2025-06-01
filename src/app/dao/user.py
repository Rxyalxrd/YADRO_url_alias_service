from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.auth.validators import hash_password


class UserRepository:
    """
    Репозиторий для работы с пользователями в базе данных.

    Позволяет выполнять операции получения пользователя по email
    и добавления нового пользователя с захешированным паролем.

    """

    def __init__(self, session: AsyncSession):
        """
        Инициализация репозитория пользователя.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy для работы с БД.

        """

        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """
        Получает пользователя по его email из базы данных.

        Args:
            email (str): Email пользователя для поиска.

        Returns:
            User | None: Объект пользователя, если найден, иначе None.

        """

        stmt = select(User).where(User.email == email)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
    
    async def add_new_user(self, email: str, password: str) -> User | None:
        """
        Добавляет нового пользователя в базу данных с захешированным паролем.

        Args:
            email (str): Email нового пользователя.
            password (str): Пароль пользователя в открытом виде.

        Returns:
            User: Созданный и сохранённый объект пользователя.

        """

        stmt = User(
            email=email,
            password=hash_password(password)
        )

        self.session.add(stmt)
        await self.session.commit()
        await self.session.refresh(stmt)

        return stmt

