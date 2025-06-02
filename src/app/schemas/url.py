from pydantic import (
    BaseModel,
    HttpUrl,
)


class URLRequest(BaseModel):
    """
    Схема запроса для сокращения исходной ссылки.

    Attributes:
        url (HttpUrl): Исходная (оригинальная) ссылка, которую необходимо сократить.

    """

    url: HttpUrl


class ClickStatResponse(BaseModel):
    last_hour_clicks: int
    last_day_clicks: int

    class Config:
        from_attributes = True


class URLResponse(BaseModel):
    """
    Схема ответа с данными о сокращённой ссылке.

    Attributes:
        url (HttpUrl): Оригинальная ссылка.
        short_url (HttpUrl): Сокращённая ссылка.
        is_activated (bool): Флаг, указывающий, активна ли ссылка.
        is_old (bool): Флаг, указывающий, считается ли ссылка устаревшей.
        last_hour_clicks (int): Количество переходов по ссылке за последний час.
        last_day_clicks (int): Количество переходов по ссылке за последние 24 часа.

    """

    original_url: HttpUrl
    short_url: str
    is_activated: bool
    is_old: bool
    stats: ClickStatResponse

    class Config:
        from_attributes = True
