import sys

from pydantic import BaseSettings


class Settings(BaseSettings):
    api_key: str = ""
    db_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SETTINGS = Settings()


LONG_LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level>| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

SHORT_LOG_FORMAT = "<level>{level:<8}</level>| <cyan>{function:20}</cyan> | <level>{message}</level>"

STDERR_HANDLER = [
    {
        "sink": sys.stderr,
        "format": SHORT_LOG_FORMAT,
        "backtrace": True,
        "diagnose": True,
    },
]

LOGFILE_HANDLER = [
    {
        "sink": "hex.log",
        "format": LONG_LOG_FORMAT,
        "backtrace": True,
        "diagnose": True,
    },
]

log_config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "format": SHORT_LOG_FORMAT,
            "backtrace": True,
            "diagnose": True,
            "level": "DEBUG",
        },
        {
            "sink": "hex.log",
            "format": LONG_LOG_FORMAT,
            "backtrace": True,
            "diagnose": True,
        },
    ],
}
