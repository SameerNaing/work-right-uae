from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.llm.agents import mohre_agent

router = APIRouter(
    prefix="/v1/chat",
    tags=["Chat"],
    dependencies=[],
)


@router.post("", response_class=StreamingResponse)
async def chat():
    return StreamingResponse(
        mohre_agent.chat("Hello My name is Naing Ye Oo, how are you ?"),
        media_type="text/plain",
    )
