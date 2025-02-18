from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.core.db import get_db
from app.core.config import settings
from app.schemas.v1.base import GeneralResponseSchema, ValidationErrorResponseSchema
from app.schemas.v1.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    RequestOtpReqSchema,
    RequestOtpResSchema,
    JwtPayloadSchema,
)
from app.core.redis import get_redis_client
from app.services import auth_service
from app.dependencies.guards import AuthGuard


router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    summary="Endpoint to login",
    response_model=GeneralResponseSchema[LoginResponseSchema],
    responses={422: {"model": ValidationErrorResponseSchema}},
)
async def login(
    request: Request, body: LoginRequestSchema, db: AsyncSession = Depends(get_db)
):
    refresh_token, access_token = await auth_service.login(
        redis=request.app.state.redis,
        db=db,
        otp=body.otp,
        otp_request_id=body.otp_request_id,
        email=body.email,
    )

    return GeneralResponseSchema.format(
        message="Login Successful",
        data=LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post(
    "/request-otp",
    summary="Send Email OTP",
    status_code=201,
    response_model=GeneralResponseSchema[RequestOtpResSchema],
    responses={422: {"model": ValidationErrorResponseSchema}},
)
async def send_otp(
    request: Request,
    body: RequestOtpReqSchema,
):

    id = await auth_service.send_otp(request.app.state.redis, body.email)
    return GeneralResponseSchema.format(
        message="OTP Sent",
        data=RequestOtpResSchema(
            otp_request_id=id,
        ),
    )


@router.post(
    "/refresh",
    summary="Endpoint to refresh access-token with refresh-token",
    description="Send refresh token from the 'Authorization' header",
    status_code=200,
    response_model=GeneralResponseSchema[LoginResponseSchema],
)
async def refresh_token(request: Request):
    refresh_token, access_token = await auth_service.refresh_token(
        request.app.state.redis, request.headers.get("authorization", None)
    )
    return GeneralResponseSchema.format(
        message="Token Refreshed",
        data=LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post(
    "/logout",
    summary="Endpoint to logout",
    description="Send refresh token from the 'Authorization' header",
    status_code=200,
    response_model=GeneralResponseSchema[None],
)
async def logout(
    request: Request,
    token: JwtPayloadSchema = Depends(AuthGuard()),
):
    await auth_service.logout(request.app.state.redis, token.session_id)
    return GeneralResponseSchema.format(message="Logged Out")
