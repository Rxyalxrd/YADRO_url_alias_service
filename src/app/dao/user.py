from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import hash_password
from app.models import User


class UserRepository:
    """
    Репозиторий для работы с пользователями в базе данных.

    Позволяет выполнять операции получения пользователя по email
    и добавления нового пользователя с захешированным паролем.

    """

    @classmethod
    async def get_by_email(cls, email: str, session: AsyncSession) -> User | None:
        """
        Получает пользователя по его email из базы данных.

        Args:
            email (str): Email пользователя для поиска.

        Returns:
            User | None: Объект пользователя, если найден, иначе None.

        """

        stmt = select(User).where(User.email == email)

        result = await session.execute(stmt)

        return result.scalar_one_or_none()
    
    @classmethod
    async def add_new_user(cls, email: str, password: str, session: AsyncSession) -> User:
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
        ) # type: ignore

        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)

        return stmt

