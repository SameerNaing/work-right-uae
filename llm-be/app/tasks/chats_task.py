import asyncio
from sqlalchemy.orm import Session, joinedload
from llama_index.core import Document

from celery import shared_task
from asgiref.sync import async_to_sync

from .base import BaseTask
from app.models.chat_history_metadata import ChatHistoryMetadata
from app.models.chat.messages import MessagesModel
from app.core.constants import ChatRole, chat_history_chroma_collection
from app.services import chat_service
from app.dependencies.chroma_repo import get_chroma_repository


@shared_task(name="save_chat", base=BaseTask, queue="high_priority", bind=True)
def save_chat(
    self,
    llm_res_message: str,
    user_id: str,
    parent_msg_id: str,
):
    session: Session = self.session

    user_message = (
        session.query(MessagesModel)
        .filter(
            MessagesModel.id == parent_msg_id,
        )
        .first()
    )

    if user_message is None:
        return False

    llm_message = MessagesModel(
        message=llm_res_message,
        role=ChatRole.AGENT,
        parent_message=user_message,
        chat_id=user_message.chat_id,
        created_by_id=user_id,
    )

    session.add(llm_message)
    session.commit()
    session.refresh(llm_message)

    metadata = ChatHistoryMetadata(
        user_message_id=user_message.id,
        assistant_message_id=llm_message.id,
        user_id=user_id,
        chat_id=user_message.chat_id,
    )

    chat_text = f"User: {user_message.message}\nAssistant: {llm_message.message}"
    doc = Document(text=chat_text, metadata=metadata.model_dump())

    chroma_repo = get_chroma_repository(chat_history_chroma_collection)
    chroma_repo.add_document_to_collection(doc)

    return True
