from pydantic import BaseModel, EmailStr


class SendOtpReqSchema(BaseModel):
    email: EmailStr
