from fastapi import status
from fastapi.exceptions import HTTPException

from app.dao import UserRepository
from .validators import (
    verify_password,
    create_access_token,
)


async def login_user(
    email: str,
    password: str,
    user_repo: UserRepository,
) -> str:
    """
    Выполняет аутентификацию пользователя и возвращает JWT-токен доступа.

    Args:
        email (str): Email пользователя для входа.
        password (str): Пароль пользователя в открытом виде.
        user_repo (UserRepository): Репозиторий пользователей для доступа к данным.

    Raises:
        HTTPException: 
            - 404, если пользователь с указанным email не найден.
            - 401, если пароль неверен.

    Returns:
        str: JWT-токен доступа, содержащий email пользователя в поле "sub".

    """

    user = await user_repo.get_by_email(email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return create_access_token({"sub": user.email})

async def register_user(
    email: str,
    password: str,
    user_repo: UserRepository
) -> str:
    """
    Регистрирует нового пользователя и возвращает JWT-токен доступа.

    Args:
        email (str): Email нового пользователя.
        password (str): Пароль нового пользователя в открытом виде.
        user_repo (UserRepository): Репозиторий пользователей для доступа к данным.

    Raises:
        HTTPException:
            - 500, если произошла внутренняя ошибка при сохранении пользователя.

    Returns:
        str: JWT-токен доступа, содержащий email зарегистрированного пользователя в поле "sub".

    """

    new_user = await user_repo.add_new_user(email, password)

    if new_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка")

    return create_access_token({"sub": new_user.email})
