from sqlalchemy import Column, String, Text, CHAR
from sqlalchemy.orm import relationship

from .base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"
    email = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
