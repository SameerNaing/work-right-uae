from sqlalchemy.future import select
from sqlalchemy import func

from .base import BaseRepository
from app.models.chat.chats import ChatsModel


class ChatRepository(BaseRepository):
    async def create(self, user_id):
        chat = ChatsModel()

        chat.created_by_id = user_id

        self.db.add(chat)
        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def get_by_id(self, chat_id: str, user_id: str):
        query = select(ChatsModel).where(
            ChatsModel.id == chat_id,
            ChatsModel.deleted_at == None,
            ChatsModel.created_by_id == user_id,
        )

        chat = await self.db.execute(query)
        return chat.scalar_one_or_none()

    async def update(self, chat_id: str, user_id: str, data: dict):
        chat = await self.get_by_id(chat_id, user_id)

        if not chat:
            return None

        for key, value in data.items():
            setattr(chat, key, value)

        await self.db.commit()
        await self.db.refresh(chat)
        return chat

    async def get_all(self, user_id: str, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit

        # Query to get total count
        total_query = (
            select(func.count())
            .where(ChatsModel.deleted_at == None, ChatsModel.created_by_id == user_id)
            .order_by(ChatsModel.created_at.desc())
        )

        total_result = await self.db.execute(total_query)
        total_count = total_result.scalar()
        total_pages = (total_count + limit - 1) // limit  # Calculate total pages

        # Query to get paginated results
        query = (
            select(ChatsModel)
            .where(ChatsModel.deleted_at == None, ChatsModel.created_by_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(query)
        chats = result.scalars().all()

        return {
            "total": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit,
            "data": chats,
        }
