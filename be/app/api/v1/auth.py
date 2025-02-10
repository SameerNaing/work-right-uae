from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.db.session import get_db
from app.core.config import settings
from app.schemas.v1.base import GeneralResponseSchema, ValidationErrorResponseSchema
from app.schemas.v1.auth import (
    LoginRequestSchema,
    LoginResponseSchema,
    SendOtpReqSchema,
)


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
async def login(body: LoginRequestSchema):
    raise HTTPException(status_code=401, detail="Invalid email or password")
    # return GeneralResponseSchema.format(
    #     message="Login Successful",
    #     data=LoginResponseSchema(
    #         access_token="token",
    #         refresh_token="refresh_token",
    #     ),
    # )


@router.post(
    "/send-otp",
    summary="Send Email OTP",
    status_code=201,
    response_model=GeneralResponseSchema[None],
    responses={422: {"model": ValidationErrorResponseSchema}},
)
async def send_otp(body: SendOtpReqSchema):
    raise Exception("HELLO WORLD")
    return GeneralResponseSchema.format("OTP Sent Successfully")
