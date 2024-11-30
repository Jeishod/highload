import random
import string
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr


__all__ = ["Authorization"]


class JwtPayload(BaseModel):
    email: EmailStr
    exp: datetime | None = None


class Authorization:
    _crypto_manager: CryptContext
    _secret_key: str
    _algorythm: str
    _expires_delta: int
    oauth2_schema: OAuth2PasswordBearer

    def __init__(
        self,
        secret_key: str,
        algorythm: str,
        login_url: str,
        expires_delta: int,
        root_path: str | None = None,
    ):
        self._crypto_manager = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._secret_key = secret_key
        self._algorythm = algorythm
        self._expires_delta = expires_delta
        if root_path:
            login_url = root_path + login_url
        self.oauth2_schema = OAuth2PasswordBearer(tokenUrl=login_url)

    @staticmethod
    def generate_random_password(length: int = 8) -> str:
        """Generate random password of letters and digits.

        Args:
            length (int, optional): password length. Defaults to 8.

        Returns:
            str: random password
        """
        characters = string.ascii_letters + string.digits
        random_string = "".join(random.choice(characters) for _ in range(length))
        return random_string

    def get_password_hash(self, password: str) -> str:
        """Get hash of the provided password.

        Args:
            password (str): password

        Returns:
            str: password hash
        """
        return self._crypto_manager.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against given hashed password.

        Args:
            plain_password (str): unhashed password
            hashed_password (str): hashed password

        Returns:
            bool: True if passwords are verified, else False
        """
        return self._crypto_manager.verify(plain_password, hashed_password)

    def create_access_token(self, email: str, expires_delta: int | None = None) -> str:
        """Create JWT access token.

        Args:
            email (str): user email
            expires_delta (timedelta, optional): JWT token expiration time in seconds.
                If not provided - defaults to ACCESS_TOKEN_EXPIRE.

        Returns:
            str: JWT access token
        """
        expires_delta = expires_delta or self._expires_delta
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        jwt_payload = JwtPayload(email=email, exp=expire)
        encoded_jwt = jwt.encode(
            claims=jwt_payload.model_dump(),
            key=self._secret_key,
            algorithm=self._algorythm,
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> JwtPayload:
        """Decode JWT access token and get JWT payload.

        Args:
            token (str): JWT access token

        Returns:
            JwtPayload: JWT payload with user ID and expiration time
        """
        payload = jwt.decode(token=token, key=self._secret_key, algorithms=self._algorythm)
        return JwtPayload.model_validate(payload)
