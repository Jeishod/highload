import asyncio
import csv

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
        await self.fill_cities_table()
        await self.fill_users_table()

    @staticmethod
    async def fill_cities_table():
        """Заполнение таблицы городов. Загрузить данные из .csv файла"""
        csv_file_path = "dev/fixtures/cities.csv"
        table_name = "cities"
        with open(csv_file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовки
            for row in reader:

                query = f"""
                INSERT INTO {table_name} (
                    id,
                    name
                ) VALUES (
                    '{row[0]}',
                    '{row[1]}'
                )
                """
                try:
                    await Services.db.execute(query)
                    LOGGER.debug(f"Row added to table '{table_name}' ({row[1]})")
                except Exception as e:
                    LOGGER.error(f"Error filling table '{table_name}': {e}")

    @staticmethod
    async def fill_users_table():
        """Заполнение таблицы пользователей. Загрузить данные из .csv файла"""
        csv_file_path = "dev/fixtures/users.csv"
        table_name = "users"
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовки
            for row in reader:
                query = f"""
                INSERT INTO {table_name} (
                    id,
                    name,
                    email,
                    gender,
                    birth_date,
                    interests,
                    city_id,
                    password
                ) VALUES (
                    '{row[0]}',
                    '{row[1]}',
                    '{row[2]}',
                    '{row[3]}',
                    '{row[4]}',
                    ARRAY['{row[5]}'],
                    '{row[6]}',
                    '{row[7]}'
                )
                """
                try:
                    await Services.db.execute(query)
                    LOGGER.debug(f"Row added to table '{table_name}' ({row[1]})")
                except Exception as e:
                    LOGGER.error(f"Error filling table '{table_name}': {e}")


def main():
    app = FixtureManager()
    asyncio.run(app.upload_data())
