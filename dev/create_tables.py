import asyncio

import asyncpg
from loguru import logger as LOGGER

from app.logger import CustomLogger
from app.services import Services
from app.settings import get_settings


class FixtureManager:
    def __init__(self):
        self.config = get_settings()
        self.logger = CustomLogger.make_logger()

    async def upload_data(self):
        LOGGER.warning("Uploading data")
        await Services.db.start()
        await self.create_cities_table()
        await self.create_users_table()

    @staticmethod
    async def create_cities_table():
        """Создание таблицы городов"""
        table_name = "cities"
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            await Services.db.execute(query)
            LOGGER.debug(f"Table '{table_name}' created")
        except asyncpg.exceptions.DuplicateTableError:
            LOGGER.warning(f"Table '{table_name}' already exists.")

    @staticmethod
    async def create_users_table():
        """Создание таблицы пользователей"""
        table_name = "users"
        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(255) NOT NULL,
            birth_date DATE,
            interests TEXT[],
            city_id UUID NOT NULL REFERENCES cities(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            await Services.db.execute(query)
            LOGGER.debug(f"Table '{table_name}' created")
        except asyncpg.exceptions.DuplicateTableError:
            LOGGER.warning(f"Table '{table_name}' already exists.")


def main():
    app = FixtureManager()
    asyncio.run(app.upload_data())
