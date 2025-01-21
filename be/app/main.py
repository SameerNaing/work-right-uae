from fastapi import FastAPI

from app.core.config import settings

# routers
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router

app = FastAPI(
    version="v1",
    title="Mohre API",
    description="MOHRE Chatbot API",
    docs_url="/api",
)

app.include_router(auth_router)
app.include_router(chat_router)
