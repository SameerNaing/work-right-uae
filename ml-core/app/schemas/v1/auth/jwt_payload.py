from typing import Any, Optional
from pydantic import BaseModel


class JwtPayloadSchema(BaseModel):
    user_id: str
    exp: Optional[Any] = None
    session_id: Optional[str] = None
