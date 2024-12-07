from typing import Annotated

from fastapi import Depends
from jose import JWTError
from loguru import logger as LOGGER
from pydantic import EmailStr

from app.api.exceptions import UnauthorizedUserException
from app.api.users.logic import UsersManager
from app.api.users.schemas import GetUserResponse
from app.services import Services


def get_current_user_email(token: Annotated[str, Depends(Services.auth.oauth2_schema)]) -> EmailStr:
    """Get user email from access token.

    Args:
        token (str): access token

    Raises:
        UnauthorizedUserException: if JWT token was not decoded

    Returns:
        str: user email
    """
    try:
        jwt_payload = Services.auth.decode_access_token(token=token)
    except JWTError as exc:
        raise JWTError("Could not decode access token") from exc
    return jwt_payload.email


class UserDepends:
    async def __call__(self, email: Annotated[EmailStr, Depends(get_current_user_email)]) -> GetUserResponse:
        """Get user model.

        Args:
            email (Annotated[str, Depends): user email (via access token)

        Raises:
            UnauthorizedUserException: if user was not found by its email

        Returns:
            GetUserResponse: user model
        """
        user_db = await UsersManager.get_user_by_email(email=email)
        if not user_db:
            raise UnauthorizedUserException()
        LOGGER.debug("User authenticated: {}", email)
        return user_db
