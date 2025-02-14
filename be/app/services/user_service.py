from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.models.user import UserModel


async def get_user_profile(db: AsyncSession, user_id: str) -> UserModel:
    user_repo = UserRepository(db)
    user = await user_repo.get(filter={"id": user_id})

    return user
