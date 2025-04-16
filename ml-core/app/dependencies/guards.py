from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.utils.encryption import decode_token
from app.models.base import BaseModel
from app.schemas.v1.auth.jwt_payload import JwtPayloadSchema


class AuthGuard(HTTPBearer):
    """
    Auth guard for checking the token and session, user must login to access the protected route.

    """

    def __init__(self, auto_error: bool = True, allow_guest: bool = False):
        self.allow_guest = allow_guest
        super(AuthGuard, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JwtPayloadSchema:
        try:
            credientials: HTTPAuthorizationCredentials = await super(
                AuthGuard, self
            ).__call__(request)

            if not credientials:
                if self.allow_guest:
                    return None
                raise HTTPException(status_code=403, detail="Unauthorized")

            token = decode_token(credientials.credentials)

            redis = request.app.state.redis

            session = await redis.get(f"session:{token.session_id}")

            if not session:
                if self.allow_guest:
                    return None
                raise HTTPException(status_code=403, detail="Unauthorized")

            BaseModel.set_user_id(token.user_id)

            return token
        except Exception as e:
            if self.allow_guest:
                return None
            raise HTTPException(status_code=403, detail="Unauthorized")
