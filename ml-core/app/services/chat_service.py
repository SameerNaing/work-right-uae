from typing import Optional, List
from fastapi import HTTPException
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from llama_index.core.llms import ChatMessage, MessageRole


from app.repositories.messages_repository import MessagesRepository
from app.repositories.chat_repository import ChatRepository
from app.models.chat.messages import MessagesModel
from app.core.llm.agents import MOHREAgent
from app.core.constants import ChatRole, ChatFeedBack


# from app.tasks.chats_task import save_chat


async def give_response_feedback(
    db: AsyncSession, message_id: str, feedback: ChatFeedBack, user_id: str
) -> MessagesModel:
    message_repo = MessagesRepository(db)

    if not await message_repo.is_user_message(user_id=user_id, message_id=message_id):
        raise HTTPException(status_code=404, detail="Message not found")

    updated = await message_repo.update(message_id, {"feed_back": feedback})

    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")

    return


async def chat_llm(
    db: AsyncSession,
    message: str,
    chat_id: Optional[str] = None,
    user_id: Optional[str] = None,
):

    if not user_id:
        return MOHREAgent(), None

    message_repo = MessagesRepository(db)

    if chat_id:
        chat = await ChatRepository(db).get_by_id(chat_id, user_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

    if chat_id is None and user_id != None:
        chat_repo = ChatRepository(db)
        chat = await chat_repo.create(user_id=user_id)
        chat_id = chat.id

    user_message = await message_repo.create(
        message=message,
        role=ChatRole.USER,
        user_id=user_id,
        chat_id=chat_id,
    )

    agent = MOHREAgent(user_id=user_id, chat_id=chat_id)

    return agent, user_message


async def get_all_messages(
    db: AsyncSession,
    chat_id: str,
    user_id: str,
    page,
    limit,
) -> dict:
    message_repo = MessagesRepository(db)

    return await message_repo.get_all(
        chat_id=chat_id, user_id=user_id, page=page, limit=limit
    )


async def get_all_chats(
    db: AsyncSession, user_id: str, page: int = 1, limit: int = 10
) -> dict:
    chat_repo = ChatRepository(db)

    return await chat_repo.get_all(user_id=user_id, page=page, limit=limit)


async def rename_chat(db: AsyncSession, chat_id: str, name: str, user_id: str):
    chat_repo = ChatRepository(db)

    chat = await chat_repo.get_by_id(chat_id, user_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    await chat_repo.update(chat_id, user_id, {"name": name})

    return


async def delete_chat(db: AsyncSession, chat_id: str, user_id: str):
    chat_repo = ChatRepository(db)

    chat = await chat_repo.get_by_id(chat_id, user_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    await chat_repo.soft_delete(chat)

    return
