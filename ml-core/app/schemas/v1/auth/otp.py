from pydantic import BaseModel, EmailStr


class RequestOtpReqSchema(BaseModel):
    email: EmailStr


class RequestOtpResSchema(BaseModel):
    otp_request_id: str
