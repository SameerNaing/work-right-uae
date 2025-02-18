from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.security import APIKeyHeader


from worker.celery_app import *


from app.core.exceptions import (
    validation_exception_handler,
    http_exception_handler,
    exception_handler,
)

# routers
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.profile import router as profile_router

from app.core.redis import get_redis_client
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis_client()
    yield
    await app.state.redis.close()


app = FastAPI(
    lifespan=lifespan,
    version="v1",
    title="Mohre API",
    description="MOHRE Chatbot API",
    docs_url="/api",
)


app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(profile_router)


@app.get("/")
async def root():
    return {"message": "Server is running..."}
