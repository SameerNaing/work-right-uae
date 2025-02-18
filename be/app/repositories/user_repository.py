from typing import Literal, List, Optional, Dict, Type
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as db_select


from .base import BaseRepository
from app.models.user import UserModel


UserFields = Literal["id", "name", "email"]


class UserRepository(BaseRepository):
    async def get_by_id(
        self,
        user_id: str,
        select: Optional[List[UserFields]] = None,
    ):
        query = (
            db_select(*[getattr(UserModel, field) for field in select])
            if select
            else db_select(UserModel)
        )

        query = query.where(UserModel.id == user_id, UserModel.deleted_at == None)

        user = await self.db.execute(query)

        return user.scalar_one_or_none()

    async def get_by_email(self, email, select: Optional[List[UserFields]] = None):
        query = (
            db_select(*[getattr(UserModel, field) for field in select])
            if select
            else db_select(UserModel)
        )

        query = query.where(UserModel.email == email, UserModel.deleted_at == None)

        user = await self.db.execute(query)

        user = user.first()

        if user and select == None:
            user = user[0]

        return user

    async def create(self, email, name):
        user = UserModel(email=email, name=name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: str, data: dict) -> UserModel | None:
        user = await self.get_by_id(user_id)

        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user_id):
        user = await self.get_by_id(user_id)

        if not user:
            return False

        await self.soft_delete(user)

        return True
