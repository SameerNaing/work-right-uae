from typing import Tuple, Optional
import json
import uuid
from fastapi import HTTPException
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import encryption, comm_func
from app.repositories.user_repository import UserRepository
from app.tasks.notifications import send_email
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

    refresh_token, session_id = await __set_user_session(redis, user.id)
    access_token = __create_token(user.id, session_id)

    return refresh_token, access_token


async def send_otp(redis: Redis, email: str):
    otp_request_id = str(uuid.uuid4())
    otp = encryption.generate_otp()

    otp_data = {"email": email, "otp": otp}
    await redis.set(f"otp:{otp_request_id}", json.dumps(otp_data), ex=300)
    print(otp)

    # send_email.delay(to=email, subject="OTP", body=f"Your OTP is {otp}")
    return otp_request_id


async def refresh_token(redis: Redis, refresh_token: str):
    stored_token = await redis.get(f"refresh_token:{refresh_token}")

    if not stored_token:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    stored_token = json.loads(stored_token)
    user_id = stored_token.get("user_id")
    session_id = stored_token.get("session_id")

    await __remove_user_session(redis=redis, session_id=session_id)

    refresh_token, session_id = await __set_user_session(redis, user_id, session_id)
    access_token = __create_token(user_id, session_id)

    return refresh_token, access_token


async def logout(redis: Redis, session_id: str):
    await __remove_user_session(redis, session_id)


async def delete_profile(redis: Redis, user_id: str, db: AsyncSession):
    user_repo = UserRepository(db)

    user = await user_repo.delete(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await logout_all_sessions(redis, user_id)

    return


async def logout_all_sessions(redis: Redis, user_id: str):
    session_ids = await redis.lrange(f"user_sessions:{user_id}", 0, -1)

    for session_id in session_ids:
        await __remove_user_session(redis, session_id)


async def __remove_user_session(redis: Redis, session_id: str):
    session_data = await redis.get(f"session:{session_id}")
    session_data = json.loads(session_data)
    refresh_token = session_data.get("refresh_token")
    user_id = session_data.get("user_id")

    await redis.delete(f"refresh_token:{refresh_token}")
    await redis.delete(f"session:{session_id}")
    await redis.lrem(f"user_sessions:{user_id}", 0, session_id)


async def __set_user_session(redis: Redis, user_id: str) -> Tuple[str, str]:
    token = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    seconds_per_day = 60 * 60 * 24

    await redis.rpush(f"user_sessions:{user_id}", session_id)

    await redis.set(
        f"refresh_token:{token}",
        json.dumps({"user_id": user_id, "session_id": session_id}),
        ex=seconds_per_day * settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    await redis.set(
        f"session:{session_id}",
        json.dumps({"user_id": user_id, "refresh_token": token}),
        ex=seconds_per_day * settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    return token, session_id


def __create_token(user_id, session_id) -> str:
    access_token_payload = JwtPayloadSchema(user_id=user_id, session_id=session_id)

    access_token = encryption.create_access_token(access_token_payload)

    return access_token
