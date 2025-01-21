import uuid
from sqlalchemy import Column, String, Text, CHAR

from .base import BaseModel


class DocumentModel(BaseModel):
    __tablename__ = "document"

    text = Column(Text, nullable=False)
    hash = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
