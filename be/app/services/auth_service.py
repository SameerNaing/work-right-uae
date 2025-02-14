import json
import uuid
from fastapi import HTTPException
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import encryption, comm_func
from app.repositories.user_repository import UserRepository
from app.tasks.emails import send_email
from app.core.config import settings
from app.schemas.v1.auth import JwtPayloadSchema


async def login(
    redis: Redis, db: AsyncSession, otp_request_id: str, otp: str, email: str
):
    user_repo = UserRepository(db)

    otp_data = await redis.get(f"otp:{otp_request_id}")

    if not otp_data:
        raise HTTPException(status_code=403, detail="OTP expired")

    otp_data = json.loads(otp_data)
    actual_otp = otp_data.get("otp")
    actual_email = otp_data.get("email")

    if actual_email != email or actual_otp != otp:
        raise HTTPException(status_code=403, detail="OTP verification failed")

    await redis.delete(f"otp:{otp_request_id}")

    user = await user_repo.get_by_email(email)

    if not user:
        username = comm_func.get_username_from_email(email)
        user = await user_repo.create(email=email, name=username)

    access_token_payload = JwtPayloadSchema(user_id=str(user.id))

    refresh_token = await __set_refresh_token(redis, user.id)
    access_token = encryption.create_access_token(access_token_payload)

    return refresh_token, access_token


async def send_otp(redis: Redis, email: str):
    otp_request_id = str(uuid.uuid4())
    otp = encryption.generate_otp()

    otp_data = {"email": email, "otp": otp}
    await redis.set(f"otp:{otp_request_id}", json.dumps(otp_data), ex=300)

    send_email.delay(to=email, subject="OTP", body=f"Your OTP is {otp}")
    return otp_request_id


async def __set_refresh_token(redis: Redis, user_id: str):
    token = str(uuid.uuid4())
    seconds_per_day = 60 * 60 * 24

    await redis.set(
        f"refresh_token:{token}",
        user_id,
        ex=seconds_per_day * settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    return token
