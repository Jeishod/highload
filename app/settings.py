from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class AppStand(StrEnum):
    DEV = "dev"
    RC = "rc"
    PROD = "prod"
    TEST = "test"
    LOCAL = "local"


class _Settings(BaseSettings):
    """General service settings"""

    APP_DEBUG: bool = False
    APP_STAND: AppStand = AppStand.LOCAL
    APP_RELEASE: str = "not-set"
    APP_PUBLIC_PATH: str | None = None
    APP_SECRET_KEY: str

    AUTH_PASSWORD_ALGORYTHM: str
    AUTH_LOGIN_URL: str
    AUTH_ACCESS_TOKEN_EXPIRE: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_POOL_SIZE: int = 10
    POSTGRES_ECHO_POOL: str | bool = False
    POSTGRES_CONNECTION_RETRY_PERIOD_SECONDS: float = 5.0

    POSTGRES_NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings(env_file: str = ".env") -> _Settings:
    return _Settings(_env_file=env_file)
