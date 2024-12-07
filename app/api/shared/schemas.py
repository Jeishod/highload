from pydantic import BaseModel, Field


class GetHealthcheckResponse(BaseModel):
    status: str = Field(..., description="The health status of the service")
