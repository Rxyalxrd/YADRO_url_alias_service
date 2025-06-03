from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_session
from app.schemas import (
    RegisterRequest,
    TokenResponse,
)
from app.auth import (
    login_user,
    register_user,
)


router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    summary="Регистрация нового пользователя",
    description=(
        "Создаёт нового пользователя по email и паролю. "
        "После успешной регистрации возвращает JWT access-токен. "
        "Email должен быть уникальным. Пароль сохраняется в хешированном виде."
    ),
)
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_async_session),
) -> TokenResponse:
    """
    Регистрирует нового пользователя.

    Args:
        data (RegisterRequest): Содержит email и пароль для регистрации.
        user_repo (UserRepository): Репозиторий доступа к данным пользователей (DI через Depends).

    Returns:
        TokenResponse: JWT access-токен, выданный новому пользователю.

    """
    
    token = await register_user(data.email, data.password, session)

    return TokenResponse(access_token=token)

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Аутентификация пользователя",
    description=(
        "Авторизует пользователя по email и паролю (через form-data). "
        "Возвращает JWT access-токен при успешной проверке учётных данных."
    ),
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> TokenResponse:
    """
    Авторизует пользователя и выдаёт JWT токен.

    Args:
        form_data (OAuth2PasswordRequestForm): Стандартная схема form-data для OAuth2 (username и password).
        user_repo (UserRepository): Репозиторий доступа к данным пользователей (DI через Depends).

    Returns:
        TokenResponse: JWT access-токен, выданный авторизованному пользователю.

    """

    token = await login_user(form_data.username, form_data.password, session)

    return TokenResponse(access_token=token, token_type="bearer")
