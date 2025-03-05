from typing import Optional
from pydantic import BaseModel

from app.core.constants import ChatRole


class AgentChatRequestSchema(BaseModel):
    message: str
    chat_id: Optional[str] = None


class ChatStreamResponseSchema(BaseModel):
    message: str
    role: ChatRole
    message_id: str
    parent_message_id: str

    @staticmethod
    def get_example():
        return ChatStreamResponseSchema(
            message="Hi",
            role=ChatRole.AGENT,
            message_id="36e66a31-20e3-45fa-87fb-a205424455b2",
            parent_message_id="0d5c0da1-f03f-4cb9-8489-594a3a1a51f5",
        )
