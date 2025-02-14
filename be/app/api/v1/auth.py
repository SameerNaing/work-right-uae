from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.db.session import get_db
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

router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    summary="Login",
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
