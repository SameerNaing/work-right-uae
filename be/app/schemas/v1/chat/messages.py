from typing import Optional
from pydantic import BaseModel

from app.core.constants import ChatFeedBack


class FeedbackSchema(BaseModel):
    feedback: ChatFeedBack


class MessageResponseSchema(BaseModel):
    id: str
    message: str
    role: str
    feed_back: Optional[ChatFeedBack] = None
