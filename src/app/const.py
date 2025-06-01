from typing import Pattern
import re


EMAIL_REGEX: Pattern[str] = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

GENERATE_SHORT_LINK: int = 6