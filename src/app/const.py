import re
from typing import Pattern

EMAIL_REGEX: Pattern[str] = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

SHORT_LINK_LEN: int = 6
MIN_PASSWORD_LENGTH: int = 8
EXIT_CODE_FOR_SETTINGS: int = 1 
DAILY_JOB: int = 24
MAX_TRY_TO_GEN_SHORT_URL: int = 1000
