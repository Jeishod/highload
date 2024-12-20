from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class GetUserResponse(BaseModel):
    """
    Endpoint get(/users/{user_id})
    """

    id: UUID
    email: EmailStr = Field(min_length=5, max_length=100)
    first_name: str = Field(examples=["John"], min_length=2, max_length=100)
    last_name: str = Field(examples=["Doe"], min_length=2, max_length=100)
    gender: Gender | None = Field(examples=[Gender.MALE, Gender.FEMALE])
    birth_date: date | None = Field(examples=["1990-01-21"], default=None)
    interests: list[str] | None = Field(examples=["travel", "music", "books"], default=None)
    city: str | None = Field(examples=["Moscow", "Saint-Petersburg"], default=None)


class SearchUsersResponse(BaseModel):
    total: int
    users: list[GetUserResponse]
