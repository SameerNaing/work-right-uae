from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.models.user import UserModel


async def get_user_profile(db: AsyncSession, user_id: str) -> UserModel:
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id=user_id)

    return user


async def update_user_profile(
    user_id: str,
    db: AsyncSession,
    update_data: dict,
):
    user_repo = UserRepository(db)
    user = await user_repo.update(user_id=user_id, data=update_data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
