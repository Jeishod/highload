from urllib.parse import quote

import asyncpg
from asyncpg.pool import Pool

from app.services.base import BaseService


__all__ = ["PostgreSQL"]


class PostgreSQL(BaseService):

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 5432,
        database: str = "postgres",
        pool_size: int = 10,
    ):
        super().__init__()
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        self._pool_size = pool_size
        self._autocommit = True
        self._pool: Pool | None = None

    def _make_url(self) -> str:
        """Создать URI для подключения к базе данных"""
        return (
            f"postgresql://{quote(self._username)}:"
            f"{quote(self._password)}@{self._host}:{self._port}/{self._database}"
        )

    async def _init_pool(self, dsn: str, max_pool_size: int = 10):
        """Инициализация пула соединений с базой данных

        Args:
            dsn: URI для подключения к базе данных
            max_pool_size: Максимальный размер пула соединений
        """
        self._pool = await asyncpg.create_pool(dsn, min_size=2, max_size=max_pool_size)

    async def start(self):
        """
        Старт сервиса
        """
        dsn = self._make_url()
        await self._init_pool(dsn=dsn, max_pool_size=self._pool_size)

    async def stop(self):
        """
        Остановка сервиса
        """
        await self._pool.close()

    @property
    def pool(self) -> Pool:
        """Получение пула соединений"""
        if self._pool is None:
            raise RuntimeError("Database pool is not initialized")
        return self._pool

    async def execute(self, query: str) -> str:
        """Выполнение запроса к базе данных

        Args:
            query: SQL запрос

        Returns:
            str: результат выполнения запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.execute(query)

    async def fetchrow(self, query: str) -> asyncpg.Record:
        """Выполнить запрос к базе данных и получить результат одной строкой

        Args:
            query: SQL запрос

        Returns:
            asyncpg.Record: результат выполнения запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query)

    async def fetchval(self, query: str) -> int:
        """Выполнить запрос к базе данных и получить значение результата

        Args:
            query: SQL запрос

        Returns:
            Any: значение результата выполнения запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query)

    async def fetch(self, query: str) -> list[asyncpg.Record]:
        """Выполнить запрос к базе данных и получить результат в из нескольких строк

        Args:
            query: SQL запрос

        Returns:
            list[asyncpg.Record]: результат выполнения запроса
        """
        async with self.pool.acquire() as connection:
            return await connection.fetch(query)
