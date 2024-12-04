from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.dependencies import UserDepends
from app.api.users.logic import UsersManager
from app.api.users.schemas import GetUserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=GetUserResponse)
async def get_current_user(_current_user: Annotated[GetUserResponse, Depends(UserDepends)]):
    """Get current user."""
    return _current_user


@router.get("/get/{user_id}", response_model=GetUserResponse)
async def get_user(user_id: UUID):
    """Get user by id."""
    return await UsersManager.get_user_by_id(user_id)
