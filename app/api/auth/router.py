from typing import Annotated

from fastapi import APIRouter, Form, status
from loguru import logger as LOGGER
from pydantic import EmailStr

from app.api.auth.logic import AuthManager
from app.api.auth.schemas import JwtResponse, PostUserRegisterRequest, PostUserRegisterResponse


router = APIRouter(prefix="/auth", tags=["Auth"])
auth_manager = AuthManager()


@router.post(
    path="/register",
    response_model=PostUserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user_info: PostUserRegisterRequest):
    """
    Register a new user.

    ### Input
    - **email** [Length from 5 to 100]: user email
    - **first_name** [Length from 2 to 100]: user first name
    - **last_name** [Length from 2 to 100]: user last name
    - **password** [Length from 6 to 50]: user password
        Password must not contain email.
        It must be at least 6 alphanumeric characters or following symbols: !@#$%^&*()_+
    - **gender** ['male', 'female']: user gender
    - **birth_date**: user birth date
    - **interests**: user interests
    - **city**: user city

    ### Output
    - **id** user ID
    """
    response = await auth_manager.register(user_info=user_info)
    LOGGER.info("[User_id: {}] user registered.", response.id)
    return response


@router.post(
    path="/login",
    response_model=JwtResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    username: Annotated[EmailStr, Form(description="User email", min_length=5, max_length=100)],
    password: Annotated[str, Form(description="User password", min_length=6, max_length=50)],
):
    """
    Login by user credentials.

    ### Input
    - **username** [Length from 5 to 100]: user email
    - **password** [Length from 6 to 50]: user password

    ### Output
    - **id**: current user ID
    - **access_token**: JWT access token
    """
    response = await auth_manager.login(email=username.lower(), password=password)
    LOGGER.debug("User authenticated: {}", username)
    return response
