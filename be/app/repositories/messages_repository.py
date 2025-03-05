from typing import Literal, Optional, List
from sqlalchemy.future import select as db_select
from sqlalchemy import func

from .base import BaseRepository
from app.models.chat.chats import ChatsModel
from app.models.chat.messages import MessagesModel
from app.core.constants import ChatRole, ChatFeedBack


MessagesFields = Literal["id", "message", "role", "feed_back"]


class MessagesRepository(BaseRepository):

    async def is_user_message(self, user_id: str, message_id: str):
        """Function to check if the message belongs to the user

        Args:
            user_id (str): user id
            message_id (str): message id

        Returns:
            bool: True if the message belongs to the user, False otherwise
        """
        query = db_select(MessagesModel).where(
            MessagesModel.id == message_id,
            MessagesModel.user_id == user_id,
            MessagesModel.deleted_at == None,
        )

        message = await self.db.execute(query)
        message = message.scalar_one_or_none()

        return message != None

    async def get_by_id(
        self,
        message_id: str,
        select: Optional[List[MessagesFields]] = None,
    ):
        query = (
            db_select(*[getattr(MessagesModel, field) for field in select])
            if select
            else db_select(MessagesModel)
        )

        query = query.where(
            MessagesModel.id == message_id, MessagesModel.deleted_at == None
        )

        message = await self.db.execute(query)

        return message.scalar_one_or_none()

    async def create(
        self,
        message: str,
        role: ChatRole,
        chat_id: Optional[str] = None,
        feed_back: Optional[ChatFeedBack] = None,
        user_id: Optional[str] = None,
        parent_id: Optional[str] = None,
    ):
        message = MessagesModel(
            message=message,
            role=role,
            feed_back=feed_back,
            created_by_id=user_id,
            parent_id=parent_id,
            chat_id=chat_id,
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def update_message(self, message_id: str, text_message: str):
        message = await self.get_by_id(message_id)
        if not message:
            return None

        message.message = text_message
        await self.db.commit()

    async def update(self, message_id: str, data: dict) -> MessagesModel | None:
        message = await self.get_by_id(message_id)

        if not message:
            return None

        for field, value in data.items():
            setattr(message, field, value)

        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def get_all(
        self,
        user_id: str,
        chat_id: str,
        limit: Optional[int] = 10,
        page: Optional[int] = 1,
    ):
        offset = (page - 1) * limit

        query = db_select(MessagesModel).where(
            MessagesModel.deleted_at == None,
            MessagesModel.chat_id == chat_id,
            MessagesModel.created_by_id == user_id,
        )
        count_query = (
            db_select(func.count())
            .select_from(MessagesModel)
            .where(
                MessagesModel.deleted_at == None,
                MessagesModel.chat_id == chat_id,
                MessagesModel.created_by_id == user_id,
            )
        )

        total_result = await self.db.execute(count_query)
        total_count = total_result.scalar()
        total_pages = (total_count + limit - 1) // limit

        query = (
            query.order_by(MessagesModel.created_at.desc()).limit(limit).offset(offset)
        )

        messages_result = await self.db.execute(query)
        messages = messages_result.scalars().all()

        return {
            "total": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit,
            "data": messages,
        }
