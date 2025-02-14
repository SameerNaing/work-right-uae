from typing import Literal, List, Optional, Dict, Type
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as db_select


from .base import BaseRepository
from app.db.session import get_db
from app.models.user import UserModel


UserFields = Literal["id", "name", "email"]


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

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

        query = query.where(UserModel.id == user_id)

        user = await self.db.execute(query)

        return user.scalar_one_or_none()

    async def get_by_email(self, email, select: Optional[List[UserFields]] = None):
        query = (
            db_select(*[getattr(UserModel, field) for field in select])
            if select
            else db_select(UserModel)
        )

        query = query.where(UserModel.email == email)

        user = await self.db.execute(query)

        return user.first()[0]

    async def create(self, email, name):
        user = UserModel(email=email, name=name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self):
        pass

    async def delete(self):
        pass

    async def get_all(self):
        pass
