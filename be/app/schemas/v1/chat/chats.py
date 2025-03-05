from pydantic import BaseModel


class ChatResponseSchema(BaseModel):
    id: str
    name: str


class UpdateChatRequestSchema(BaseModel):
    name: str
