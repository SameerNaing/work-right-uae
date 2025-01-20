from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.core.config import settings


app = FastAPI(
    version="v1",
    title="Mohre API",
    description="MOHRE Chatbot API",
    docs_url="/v1/api",
)

app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
