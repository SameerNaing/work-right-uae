from typing import Optional, List
from asyncio import sleep
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.llm.agents import MOHREAgent
from app.core.db import get_db
from app.dependencies.guards import AuthGuard
from app.dependencies.stream import ChatStreamInterceptor
from app.schemas.v1.auth import JwtPayloadSchema
from app.schemas.v1.chat import (
    AgentChatRequestSchema,
    ChatStreamResponseSchema,
    FeedbackSchema,
    ChatResponseSchema,
    UpdateChatRequestSchema,
    MessageResponseSchema,
)
from app.schemas.v1.base import (
    ValidationErrorResponseSchema,
    GeneralResponseSchema,
    PaginateResponseSchema,
)
from app.services import chat_service


router = APIRouter(
    prefix="/v1/chats",
    tags=["Chat"],
    dependencies=[],
)


@router.post(
    "/chat",
    response_model=ChatStreamResponseSchema,
    summary="Chat with Agent",
    responses={
        422: {"model": ValidationErrorResponseSchema},
        200: {
            "model": ChatStreamResponseSchema,
            "content": {
                "text/event-stream": {
                    "example": f"{ChatStreamResponseSchema.get_example().model_dump_json()}\n\n"
                }
            },
        },
    },
)
async def chat(
    body: AgentChatRequestSchema,
    db: AsyncSession = Depends(get_db),
    token: Optional[JwtPayloadSchema] = Depends(AuthGuard(allow_guest=True)),
):

    agent, user_message = await chat_service.chat_llm(
        db=db,
        message=body.message,
        chat_id=body.chat_id,
        user_id=token.user_id if token else None,
    )

    return StreamingResponse(
        ChatStreamInterceptor(
            stream=agent.chat(query=body.message),
            user_message=user_message,
            user_id=token.user_id if token else None,
        ),
        media_type="text/event-stream",
    )


@router.get(
    "",
    response_model=PaginateResponseSchema[List[ChatResponseSchema]],
    summary="Get all chats",
    dependencies=[Depends(AuthGuard())],
)
async def get_chats(
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
    page: int = 1,
    limit: int = 10,
):
    res = await chat_service.get_all_chats(
        db=db, page=page, limit=limit, user_id=token.user_id
    )

    return PaginateResponseSchema.format(message="Chats retrieved successfully", **res)


@router.patch(
    "/{chat_id}",
    response_model=GeneralResponseSchema[None],
    summary="Rename chat",
    dependencies=[Depends(AuthGuard())],
)
async def rename_chat(
    chat_id: str,
    body: UpdateChatRequestSchema,
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
):
    await chat_service.rename_chat(
        db=db, chat_id=chat_id, name=body.name, user_id=token.user_id
    )

    return GeneralResponseSchema.format(message="Chat renamed successfully")


@router.delete(
    "/{chat_id}",
    response_model=GeneralResponseSchema[None],
    summary="Delete chat",
    dependencies=[Depends(AuthGuard())],
)
async def delete_chat(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
):
    await chat_service.delete_chat(db=db, chat_id=chat_id, user_id=token.user_id)

    return GeneralResponseSchema.format(message="Chat deleted successfully")


@router.get(
    "/{chat_id}/messages",
    response_model=PaginateResponseSchema[List[MessageResponseSchema]],
    dependencies=[Depends(AuthGuard())],
    summary="Get all messages",
)
async def get_messages(
    chat_id: str,
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
    page: int = 1,
    limit: int = 10,
):
    res = await chat_service.get_all_messages(
        db=db, chat_id=chat_id, user_id=token.user_id, page=page, limit=limit
    )

    return PaginateResponseSchema.format(
        message="Messages retrieved successfully", **res
    )


@router.patch(
    "/message-feedback/{message_id}",
    response_model=GeneralResponseSchema[None],
)
async def feedback(
    message_id: str,
    body: FeedbackSchema,
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
):
    await chat_service.give_response_feedback(
        db=db, feedback=body.feedback, user_id=token.user_id, message_id=message_id
    )

    return GeneralResponseSchema.format(message="Feedback submitted successfully")
