from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.const import MIN_PASSWORD_LENGTH

class RegisterRequest(BaseModel):
    """
    Схема запроса для регистрации нового пользователя.

    Attributes:
        email (EmailStr): Адрес электронной почты пользователя.
        password (str): Пароль пользователя (в незахешированном виде).

    """

    email: EmailStr
    password: str = Field(..., ge=MIN_PASSWORD_LENGTH)


class TokenResponse(BaseModel):
    """
    Схема ответа, содержащего JWT-токен после регистрации или авторизации.

    Attributes:
        access_token (str): Сгенерированный JWT-токен.
        token_type (str): Тип токена (по умолчанию 'Bearer').

    """

    access_token: str
    token_type: str = "Bearer"
