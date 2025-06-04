import re
from typing import Pattern


EXIT_CODE_FOR_SETTINGS: int = 1

SHORT_LINK_LEN: int = 6
MIN_PASSWORD_LENGTH: int = 8
MAX_TRY_TO_GEN_SHORT_URL: int = 1000

EMAIL_REGEX: Pattern[str] = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

DAILY_JOB: int = 24
HOURLY_JOB: int = 1