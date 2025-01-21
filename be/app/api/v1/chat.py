from fastapi import APIRouter

router = APIRouter(
    prefix="/v1/chat",
    tags=["Chat"],
    dependencies=[],
)


@router.get("/chat")
async def chat():
    return {"message": "AI Chat"}
