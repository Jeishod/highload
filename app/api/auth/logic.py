from uuid import UUID

from fastapi import HTTPException, status
from loguru import logger as LOGGER

from app.api.auth.schemas import JwtResponse, PostUserRegisterRequest, PostUserRegisterResponse, UserWithPasswordSchema
from app.services import Services


class AuthManager:
    """Authorization manager"""

    @staticmethod
    async def check_user_email(email: str):
        """Check if user with such email already exists

        Args:
            email (str): user email

        Returns:
            UserWithPasswordSchema | None: user info
        """
        email = email.lower()
        get_user_by_email_query = f"""
            SELECT u.id FROM users u WHERE u.email = '{email}'
        """
        user_existing = await Services.db.fetchrow(query=get_user_by_email_query)
        if user_existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with such email {email} already exists.",
            )

    @staticmethod
    async def validate_city(city: str) -> UUID | None:
        """Validate existing city

        Args:
            city (str): city name

        Returns:
            UUID | None: city id
        """
        validate_city_query = f"""
            SELECT c.id FROM cities c WHERE c.name ILIKE '{city}'
        """
        city_id = await Services.db.fetchrow(query=validate_city_query)
        if not city_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"City {city} not found.",
            )
        return city_id["id"]

    async def register(self, user_info: PostUserRegisterRequest) -> PostUserRegisterResponse:
        """Logic of endpoint POST `/auth/register`

        Args:
            user_info (pydantic.PostRegisterRequest): info about the user to create

        Raises:
            pydantic.ObjectAlreadyExists: if user with such email already exists

        Returns:
            pydantic.PostRegisterResponse: registered user
        """
        await self.check_user_email(email=user_info.email)
        city_id = None
        if user_info.city:
            city_id = await self.validate_city(city=user_info.city)
        password_hash = Services.auth.get_password_hash(password=user_info.password)
        interests_array = f"{{{user_info.interests}}}" if user_info.interests else "{}"
        LOGGER.debug(f"City id: {city_id}")
        create_user_query = f"""
            INSERT INTO users (
                email,
                first_name,
                last_name,
                password,
                gender,
                birth_date,
                interests,
                city_id
            )
            VALUES (
                '{user_info.email}',
                '{user_info.first_name}',
                '{user_info.last_name}',
                '{password_hash}',
                '{user_info.gender}',
                '{user_info.birth_date}',
                '{interests_array}',
                '{city_id}'
            )
            RETURNING id
        """
        user_id = await Services.db.fetchrow(query=create_user_query)
        return PostUserRegisterResponse(id=user_id["id"])

    @staticmethod
    async def login(email: str, password: str) -> JwtResponse:
        """Logic of endpoint POST `/auth/login`

        Args:
            email (str): user email
            password (str): user password

        Raises:
            pydantic.AuthenticationFailed: if user is not found by email or password is invalid

        Returns:
            pydantic.PostLoginResponse: access token
        """
        get_user_by_email_query = f"""
            SELECT u.id, u.email, u.password FROM users u WHERE u.email = '{email}'
        """
        user = await Services.db.fetchrow(query=get_user_by_email_query)
        if not user:
            LOGGER.debug(f"User {email} failed to authenticate. Not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Cannot login with email {email}.",
            )
        db_user = UserWithPasswordSchema(**user)
        if not Services.auth.verify_password(
            plain_password=password, hashed_password=db_user.password.get_secret_value()
        ):
            LOGGER.debug(f"User {email} failed to authenticate. Incorrect password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Cannot login with email {email}.",
            )
        access_token = Services.auth.create_access_token(email=db_user.email)
        return JwtResponse(id=db_user.id, access_token=access_token)
