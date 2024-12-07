from fastapi import APIRouter

from app.api.shared.schemas import GetHealthcheckResponse


router = APIRouter(prefix="/shared", tags=["Shared"])


@router.get("/healthcheck")
async def healthcheck():
    """Healthcheck endpoint."""
    return GetHealthcheckResponse(status="ok")
