from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.v1.base import ValidationErrorResponseSchema, GeneralResponseSchema


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    res = ValidationErrorResponseSchema.format(exc.errors())
    return JSONResponse(
        status_code=422,
        content=res.model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    res = GeneralResponseSchema.format(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=res.model_dump(),
    )


async def exception_handler(request: Request, exc: HTTPException):
    res = GeneralResponseSchema.format("Something went wrong")
    return JSONResponse(
        status_code=500,
        content=res.model_dump(),
    )
