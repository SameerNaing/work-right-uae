from typing import List
from sqlalchemy import Column, String, Text, CHAR
from sqlalchemy.orm import relationship, mapped_column, Mapped

from .base import BaseModel
from .chat.messages import MessagesModel


class UserModel(BaseModel):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
