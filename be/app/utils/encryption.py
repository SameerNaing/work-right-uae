import random
import string
import datetime
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.schemas.v1.auth import JwtPayloadSchema


def parse_token(token: str):
    if "Bearer" in token:
        return token.split("Bearer ")[-1]
    return token


def create_access_token(data: JwtPayloadSchema):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        days=settings.JWT_ACCESS_TOKEN_EXPIRE_DAYS
    )
    data.exp = expire

    return jwt.encode(
        data.model_dump(), settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str, throw_error=True):
    try:
        data = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return JwtPayloadSchema(**data)
    except:
        if throw_error:
            raise InvalidTokenError("Invalid Token")
        return None


def generate_otp(length=6):
    return "".join(random.choices(string.digits, k=length))
