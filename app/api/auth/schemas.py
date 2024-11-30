import re
from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


class PatchUserRequest(BaseModel):
    """
    Endpoint patch(/users/me)
    Endpoint get(/users/me)
    """

    first_name: str = Field(examples=["John"])
    last_name: str = Field(examples=["Doe"])


class PostUserRegisterRequest(BaseModel):
    """
    Endpoint post(/auth/register)
    """

    email: EmailStr = Field(min_length=5, max_length=100)
    name: str = Field(examples=["John Doe"], min_length=2, max_length=100)
    password: str = Field(examples=["password123"], min_length=6, max_length=50)
    gender: str = Field(examples=["male", "female"], min_length=4, max_length=6)
    birth_date: date | None = Field(examples=["1990-01-01"], default=None)
    interests: str | None = Field(examples=["travel", "music", "books"], default=None)
    city: str | None = Field(examples=["Moscow", "Saint-Petersburg"], default=None)

    @validator("password")
    def validate_password(cls, password, values) -> str:
        if not re.match(r"[\w!@#$%^&*()_+]{6,}", password):
            raise ValueError("Password should be at least 6 alphanumeric characters or following symbols: !@#$%^&*()_+")
        # Check that email is in values cause if EmailStr validation fails, it is missing from values
        if "email" in values and values["email"] in password:
            raise ValueError("Password should not contain email")
        return password


class PostUserRegisterResponse(BaseModel):
    """
    Endpoint post(/auth/register)
    """

    id: UUID


class UserWithPasswordSchema(BaseModel):
    id: UUID
    email: EmailStr
    password: SecretStr


class JwtResponse(BaseModel):
    """
    Endpoint post(/auth/jwt/login)
    Endpoint post(/auth/jwt/refresh)
    """

    id: UUID
    access_token: str
