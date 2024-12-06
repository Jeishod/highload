from uuid import UUID

from fastapi import HTTPException, status
from loguru import logger as LOGGER
from pydantic import EmailStr

from app.api.users.schemas import GetUserResponse, SearchUsersResponse
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

    @staticmethod
    async def get_user_by_email(email: EmailStr) -> GetUserResponse:
        query = f"""
        SELECT u.id, u.email, u.name, u.gender, u.birth_date, u.interests, u.city_id, c.name as city
        FROM users u
        LEFT JOIN cities c ON u.city_id = c.id
        WHERE u.email = '{email}'
        """
        user = await Services.db.fetchrow(query=query)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return GetUserResponse(**user)

    @staticmethod
    async def search_users(
        first_name: str | None = None, last_name: str | None = None, limit: int = 100, offset: int = 0
    ) -> SearchUsersResponse:
        if not first_name and not last_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="First name or last name are required")

        conditions = []
        if first_name is not None:
            conditions.append(f"u.first_name ILIKE '%{first_name}%'")
        if last_name is not None:
            conditions.append(f"u.last_name ILIKE '%{last_name}%'")
        where_clause = " AND ".join(conditions)

        query = f"""
        SELECT u.id, u.email, u.first_name, u.last_name, u.gender, u.birth_date, u.interests, u.city_id, c.name as city
        FROM users u
        LEFT JOIN cities c ON u.city_id = c.id
        WHERE {where_clause}
        ORDER BY u.id
        LIMIT {limit} OFFSET {offset}
        """
        users = await Services.db.fetch(query=query)
        total_count = await Services.db.fetchval(query=f"SELECT COUNT(*) FROM users u WHERE {where_clause}")
        return SearchUsersResponse(users=[GetUserResponse(**user) for user in users], total=total_count)
