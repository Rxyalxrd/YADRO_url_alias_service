from fastapi import (
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jose import (
    jwt,
    JWTError,
)

from app.core import (
    get_async_session,
    settings,
)
from app.dao import UserRepository
from app.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Извлекает текущего аутентифицированного пользователя из JWT-токена.

    Args:
        token (str): JWT-токен, полученный из заголовка Authorization.
        user_repo (UserRepository): Репозиторий пользователей для поиска пользователя.

    Raises:
        HTTPException: 
            - 401 Unauthorized, если токен отсутствует, недействителен или не содержит email.
            - 404 Not Found, если пользователь с email из токена не найден.

    Returns:
        User: Модель пользователя, соответствующая email из токена.

    """

    try:
        payload = jwt.decode(token, settings.hash_secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token decode error")

    user = await UserRepository.get_by_email(email, session)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
