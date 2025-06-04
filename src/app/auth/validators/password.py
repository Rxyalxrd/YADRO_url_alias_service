import datetime as dt

from jose import jwt
from passlib.context import CryptContext

from app.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль с помощью bcrypt.

    Args:
        password (str): Пароль в открытом виде.

    Returns:
        str: Захэшированная версия пароля, готовая для хранения в базе данных.

    """

    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Проверяет совпадение открытого пароля и захэшированного пароля.

    Args:
        plain_password (str): Пароль в открытом виде, введённый пользователем.
        hashed_password (str): Захэшированный пароль из базы данных.

    Returns:
        bool: True, если пароли совпадают, иначе False.

    """

    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    data: dict,
    expires_delta: dt.timedelta | None = None
) -> str:
    """
    Создаёт JWT-токен доступа с указанными данными и временем истечения срока.

    Args:
        data (dict): Полезная нагрузка (payload) токена, например, {"sub": email}.
        expires_delta (timedelta | None): Время жизни токена. Если None, берётся значение из настроек.

    Returns:
        str: Закодированный JWT-токен в виде строки.

    """

    expire = (
        dt.datetime.now(dt.timezone.utc) +
        (
            expires_delta or
            dt.timedelta(minutes=settings.access_token_expire_minutes)
            )
    )
    data.update({"exp": expire})

    return jwt.encode(data, settings.hash_secret_key, algorithm=settings.algorithm)
