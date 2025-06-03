from sys import exit

from pydantic import (
    PostgresDsn,
    ValidationError,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from loguru import logger

from app.const import EXIT_CODE_FOR_SETTINGS

class FastAPISettings(BaseSettings):
    """
    Настройки `FastAPI` приложения.

    Attributes
    ----------
    app_title : str
        Название приложения.
    app_description : str
        Описание приложения.
    secret : str
        Секретный ключ приложения, используется для подписи JWT и других нужд.

    """

    app_host: str
    app_port: int
    app_title: str
    app_description: str


class PostgreSQLSettings(BaseSettings):
    """
    Настройки подключения к базе данных PostgreSQL.

    Attributes
    ----------
    postgres_user : str
        Имя пользователя БД.
    postgres_password : str
        Пароль пользователя БД.
    postgres_host : str
        Хост, на котором работает сервер БД.
    postgres_port : int
        Порт сервера БД.
    postgres_db : str
        Название базы данных.

    Methods
    -------
    database_url()
        Составляет полный url для подключения к БД.

    """

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db: str

    @property
    def database_url(self) -> str:
        """
        Формирует строку подключения к базе данных PostgreSQL
        с использованием драйвера asyncpg.

        Returns
        -------
        str
            Строка подключения в формате:
            postgresql+asyncpg://user:password@host:port/db

        """

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db
        ).unicode_string()



class JWTSettings(BaseSettings):
    """
    Настройки генерации токенов.

    Attributes
    ----------
        hash_secret_key: str
            Секретный ключ для генерации токенов.
        algorithm: str
            Алгоритм шифрования JWT.
        access_token_expire_minutes: int
            Время жизни токена в минутах.

    """

    hash_secret_key: str
    algorithm: str
    access_token_expire_minutes: int

class Settings(
    FastAPISettings,
    PostgreSQLSettings,
    JWTSettings,
):
    """
    Основные настройки проекта, загружаемые из .env файла.

    Attributes
    ----------
    model_config : SettingsConfigDict
        Конфигурация загрузки настроек из .env файла.

    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

try:
    settings = Settings() # type: ignore
    logger.success("Загрузка настроек прошла успешно...")
except ValidationError:
    logger.error("Ошибка в загрузке настроек, проверьте .env")
    exit(EXIT_CODE_FOR_SETTINGS)
