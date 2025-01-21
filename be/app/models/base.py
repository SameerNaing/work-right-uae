import uuid
from sqlalchemy import Column, CHAR

from app.db.session import Base


class BaseModel(Base):
    __abstract__ = True

    userId: str

    @staticmethod
    def set_user_id(user_id: str):
        BaseModel.userId = user_id

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
