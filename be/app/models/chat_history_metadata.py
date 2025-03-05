from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatHistoryMetadata(BaseModel):
    user_message_id: str
    assistant_message_id: str
    chat_id: str
    user_id: str
