from typing import Optional
from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    email: str
    name: str
    id: str


class UpdateUserRequestSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
