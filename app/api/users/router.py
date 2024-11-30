from uuid import UUID

from fastapi import APIRouter

from app.api.users.logic import UsersManager
from app.api.users.schemas import GetUserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/get/{user_id}", response_model=GetUserResponse)
async def get_user(user_id: UUID):
    return await UsersManager.get_user_by_id(user_id)
