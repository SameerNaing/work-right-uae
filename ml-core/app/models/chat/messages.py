from typing import List, Optional
from sqlalchemy import Column, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.core.constants import ChatRole, ChatFeedBack
from ..base import BaseModel


class MessagesModel(BaseModel):
    __tablename__ = "messages"

    message: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[ChatRole] = mapped_column(Enum(ChatRole), nullable=False)
    feed_back: Mapped[Optional[ChatFeedBack]] = mapped_column(
        Enum(ChatFeedBack), nullable=True
    )
    # relations

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("messages.id"), nullable=True
    )

    parent_message: Mapped[Optional["MessagesModel"]] = relationship(
        "MessagesModel",
        remote_side="MessagesModel.id",  # Points to the primary key
        back_populates="responses",
    )

    responses: Mapped[List["MessagesModel"]] = relationship(
        "MessagesModel", back_populates="parent_message"
    )

    chat_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("chats.id"), nullable=True
    )

    chat: Mapped[Optional["ChatsModel"]] = relationship(
        "ChatsModel",
        back_populates="messages",
        foreign_keys=[chat_id],
    )
