from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.core.db import get_db
from app.core.config import settings
from app.services import user_service, auth_service
from app.dependencies.guards import AuthGuard
from app.schemas.v1.auth import (
    JwtPayloadSchema,
    UserResponseSchema,
    UpdateUserRequestSchema,
)
from app.schemas.v1.base import GeneralResponseSchema

oauth2_scheme = APIKeyHeader(
    name="Authorization", auto_error=False, description='Put "Bearer <token>"'
)


router = APIRouter(
    prefix="/v1/profile",
    tags=["Profile"],
)


@router.get(
    "/me",
    summary="Get logged in user profile",
    dependencies=[Depends(AuthGuard())],
    response_model=GeneralResponseSchema[UserResponseSchema],
)
async def get_me(
    db: AsyncSession = Depends(get_db), token: JwtPayloadSchema = Depends(AuthGuard())
):

    user = await user_service.get_user_profile(db=db, user_id=token.user_id)

    return GeneralResponseSchema.format(
        message="User profile retrieved successfully",
        data=UserResponseSchema.model_validate(user, from_attributes=True),
    )


@router.patch(
    "/me",
    summary="Update logged in user profile",
    response_model=GeneralResponseSchema[UserResponseSchema],
)
async def update_me(
    db: AsyncSession = Depends(get_db),
    token: JwtPayloadSchema = Depends(AuthGuard()),
    body: UpdateUserRequestSchema = Depends(),
):

    updated_user = await user_service.update_user_profile(
        user_id=token.user_id,
        db=db,
        update_data=body.model_dump(exclude_unset=True, exclude_none=True),
    )

    return GeneralResponseSchema.format(
        message="Profile updated successfully",
        data=UserResponseSchema.model_validate(updated_user, from_attributes=True),
    )


@router.delete(
    "/me",
    summary="Delete logged in user profile",
    response_model=GeneralResponseSchema[None],
)
async def delete_me(
    request: Request,
    token: JwtPayloadSchema = Depends(AuthGuard()),
    db: AsyncSession = Depends(get_db),
):
    await auth_service.delete_profile(
        redis=request.app.state.redis,
        user_id=token.user_id,
        db=db,
        session_id=token.session_id,
    )

    return GeneralResponseSchema.format(message="Profile deleted successfully")
