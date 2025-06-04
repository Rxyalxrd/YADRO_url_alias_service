from fastapi import status
from fastapi.exceptions import HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import (
    create_access_token,
    verify_password,
)
from app.dao import UserRepository


async def login_user(
    email: str,
    password: str,
    session: AsyncSession,
) -> str:
    """
    Выполняет аутентификацию пользователя и возвращает JWT-токен доступа.

    Args:
        email (str): Email пользователя для входа.
        password (str): Пароль пользователя в открытом виде.

    Raises:
        HTTPException: 
            - 404, если пользователь с указанным email не найден.
            - 401, если пароль неверен.

    Returns:
        str: JWT-токен доступа, содержащий email пользователя в поле "sub".

    """

    logger.info("Начинаем аутентификацию пользователя.")

    try:
        user = await UserRepository.get_by_email(email, session)

    except Exception:
        logger.critical("Не удалось получить пользователя по email")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось получить пользователя по email",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден")

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль"
        )
    
    logger.info("Генерируем токен для пользователя")

    return create_access_token({"sub": user.email})


async def register_user(
    email: str,
    password: str,
    session: AsyncSession,
) -> str:
    """
    Регистрирует нового пользователя и возвращает JWT-токен доступа.

    Args:
        email (str): Email нового пользователя.
        password (str): Пароль нового пользователя в открытом виде.
        user_repo (UserRepository): Репозиторий пользователей для доступа к данным.

    Raises:
        HTTPException: 500 - Внутренняя ошибка при сохранении пользователя.

    Returns:
        str: JWT-токен доступа, содержащий email зарегистрированного пользователя в поле "sub".

    """

    logger.info("Начинаем регистрацию пользователя")
    
    try:
        new_user = await UserRepository.add_new_user(email, password, session)

    except Exception:
        logger.critical("Ошибка регистрации")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка регистрации",
        )
    
    logger.info("Генерируем токен для пользователя")

    return create_access_token({"sub": new_user.email})
