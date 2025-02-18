from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from app.utils.encryption import decode_token
from app.models.base import BaseModel
from app.schemas.v1.auth.jwt_payload import JwtPayloadSchema


class AuthGuard(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AuthGuard, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JwtPayloadSchema:
        try:
            credientials: HTTPAuthorizationCredentials = await super(
                AuthGuard, self
            ).__call__(request)
            if not credientials:
                raise HTTPException(status_code=403, detail="Unauthorized")

            token = decode_token(credientials.credentials)

            redis = request.app.state.redis

            session = await redis.get(f"session:{token.session_id}")

            if not session:
                raise HTTPException(status_code=403, detail="Unauthorized")

            BaseModel.set_user_id(token.user_id)

            return token
        except Exception as e:
            raise HTTPException(status_code=403, detail="Unauthorized")
