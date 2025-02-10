from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from worker.celery_app import *

from app.core.exceptions import (
    validation_exception_handler,
    http_exception_handler,
    exception_handler,
)

# routers
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router


app = FastAPI(
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
