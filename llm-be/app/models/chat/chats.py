from typing import List, Optional
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped


from app.core.constants import ChatRole, ChatFeedBack
from ..base import BaseModel
from .messages import MessagesModel


class ChatsModel(BaseModel):
    __tablename__ = "chats"

    name: Mapped[str] = mapped_column(Text, default="New Chat")
    messages: Mapped[List["MessagesModel"]] = relationship(
        "MessagesModel",
        back_populates="chat",
        foreign_keys=MessagesModel.chat_id,
    )
