from typing import Pattern
import re


EMAIL_REGEX: Pattern[str] = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

SHORT_LINK_LEN: int = 6
MIN_PASSWORD_LENGTH: int = 8
