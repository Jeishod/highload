from uuid import UUID

from fastapi import HTTPException, status
from loguru import logger as LOGGER

from app.api.users.schemas import GetUserResponse
from app.services import Services


class UsersManager:
    """Users manager"""

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> GetUserResponse:
        query = f"""
        SELECT u.id, u.email, u.name, u.gender, u.birth_date, u.interests, u.city_id, c.name as city
        FROM users u
        LEFT JOIN cities c ON u.city_id = c.id
        WHERE u.id = '{user_id}'
        """
        user = await Services.db.fetchrow(query=query)
        LOGGER.debug(f"User {user_id} found: {user}")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return GetUserResponse(**user)
