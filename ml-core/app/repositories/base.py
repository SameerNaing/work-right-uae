import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.base import BaseModel
from app.models.user import UserModel


class BaseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def soft_delete(self, model: BaseModel):
        model.deleted_at = datetime.datetime.now(datetime.timezone.utc)

        user = await self.db.execute(
            select(UserModel).where(UserModel.id == BaseModel.user_id)
        )
        model.deleted_by = user.scalar_one_or_none()

        self.db.add(model)
        await self.db.commit()
        return model
