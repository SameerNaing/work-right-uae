import json
import asyncio
from typing import AsyncGenerator, Optional
from concurrent.futures import ThreadPoolExecutor
import threading
from llama_index.core.llms import ChatMessage, MessageRole


from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.messages_repository import MessagesRepository
from app.core.constants import ChatRole
from app.schemas.v1.chat.agent_chat import ChatStreamResponseSchema
from app.tasks.chats_task import save_chat
from app.models.chat.messages import MessagesModel
from app.services import chat_service


class ChatStreamInterceptor:
    def __init__(
        self,
        stream: AsyncGenerator,
        user_id: Optional[str],
        user_message: Optional[MessagesModel],
    ):
        self.user_id = user_id
        self.stream = stream
        self.user_message = user_message

    def __iter__(self):
        try:

            text = ""
            for token in self.stream:
                text += token
                yield f"data: {token}\n\n"

            if self.user_id == None:
                return

            save_chat.delay(
                llm_res_message=text,
                user_id=self.user_id,
                parent_msg_id=self.user_message.id,
            )

        except Exception as e:
            print(e)
            yield json.dumps({"error": "Internal Server Error"})
