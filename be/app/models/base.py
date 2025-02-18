from datetime import datetime
import uuid
from sqlalchemy import Column, CHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    user_id: str

    @staticmethod
    def set_user_id(user_id: str):
        BaseModel.user_id = user_id

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )

    deleted_at = Column(DateTime, nullable=True)
    deleted_by_id = Column(CHAR(36), ForeignKey("user.id"), nullable=True)

    @declared_attr
    def deleted_by(cls):
        return relationship(
            "UserModel",
            foreign_keys=[cls.deleted_by_id],
            remote_side="UserModel.id",
            post_update=True,
        )
