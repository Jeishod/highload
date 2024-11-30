import inspect
from typing import Type

from app.services.auth import Authorization
from app.services.base import BaseService
from app.services.postgresql import PostgreSQL
from app.settings import get_settings


class Services:
    config = get_settings()
    db = PostgreSQL(
        username=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        pool_size=config.POSTGRES_POOL_SIZE,
    )
    auth = Authorization(
        secret_key=config.APP_SECRET_KEY,
        algorythm=config.AUTH_PASSWORD_ALGORYTHM,
        login_url=config.AUTH_LOGIN_URL,
        expires_delta=config.AUTH_ACCESS_TOKEN_EXPIRE,
        root_path=config.APP_PUBLIC_PATH,
    )

    @classmethod
    def get_external_services(cls) -> list[Type[BaseService]]:
        """
        Find all class attributes with BaseService subclass
        for using start and stop methods.
        """
        external_services = []
        for _, obj in inspect.getmembers(cls):
            if issubclass(type(obj), BaseService):
                external_services.append(obj)
        return external_services
