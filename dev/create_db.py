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
        await self.create_database()

    async def create_database(self):
        try:
            await Services.db.execute(f"CREATE DATABASE {self.config.POSTGRES_DB}")
            await Services.db.execute(
                f"GRANT ALL PRIVILEGES ON DATABASE {self.config.POSTGRES_DB} TO {self.config.POSTGRES_USER}"
            )
            LOGGER.debug("Database created")
        except asyncpg.exceptions.DuplicateDatabaseError:
            LOGGER.warning(f"Database '{self.config.POSTGRES_DB}' already exists.")


def main():
    app = FixtureManager()
    asyncio.run(app.upload_data())
