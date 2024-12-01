from fastapi import APIRouter

from app.api.shared.schemas import GetHealthcheckResponse


router = APIRouter(prefix="/shared", tags=["Shared"])


@router.get("/healthcheck")
async def healthcheck():
    return GetHealthcheckResponse(status="ok")
