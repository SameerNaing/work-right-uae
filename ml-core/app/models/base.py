from typing import Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, CHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declared_attr, mapped_column, Mapped
from sqlalchemy.sql import func

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True

    user_id: str

    @staticmethod
    def set_user_id(user_id: str):
        BaseModel.user_id = user_id

    id: Mapped[str] = mapped_column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),
        onupdate=func.now(),
    )

    created_by_id: Mapped[Optional[str]] = mapped_column(
        CHAR(36), ForeignKey("user.id"), nullable=True
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_by_id: Mapped[Optional[str]] = mapped_column(
        CHAR(36), ForeignKey("user.id"), nullable=True
    )

    @declared_attr
    def deleted_by(cls):
        return relationship(
            "UserModel",
            foreign_keys=[cls.deleted_by_id],
            remote_side="UserModel.id",
            post_update=True,
        )

    @declared_attr
    def created_by(cls):
        return relationship(
            "UserModel",
            foreign_keys=[cls.created_by_id],
            remote_side="UserModel.id",
            post_update=True,
        )
