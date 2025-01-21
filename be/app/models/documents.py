import uuid
from sqlalchemy import Column, String, Text, CHAR

from app.db.session import Base


class DocumentModel(Base):
    __tablename__ = "document"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    text = Column(Text, nullable=False)
    hash = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
