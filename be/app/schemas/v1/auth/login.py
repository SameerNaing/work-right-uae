from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    otp: str

    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v):
        if not v:
            raise ValueError("Otp should have at least 1 character")
        return v
