from fastapi import APIRouter

from app.api.auth import auth_router
from app.api.users import users_router


router = APIRouter()


router.include_router(auth_router)
router.include_router(users_router)
