import uuid

from typing import Generic, TypeVar, Optional, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")


class GeneralResponseSchema(BaseModel, Generic[T]):
    uuid: str
    messsage: str
    data: Optional[T] = None

    @staticmethod
    def format(message: str, data: Optional[T] = None):
        return GeneralResponseSchema(
            uuid=str(uuid.uuid4()),
            messsage=message,
            data=data,
        )


class PaginateResponseSchema(GeneralResponseSchema, Generic[T]):
    total: int
    page: int
    limit: int

    @staticmethod
    def format(
        message: str,
        data: Optional[T] = None,
        total: int = 0,
        page: int = 1,
        limit: int = 10,
    ):
        return PaginateResponseSchema(
            uuid=str(uuid.uuid4()),
            messsage=message,
            data=data,
            total=total,
            page=page,
            limit=limit,
        )


class ValidationErrorResponseSchema(BaseModel):
    uuid: str = Field(description="Unique identifier for the response")
    message: str = Field(description="Error message")
    validation: Dict[str, str] = Field(
        description="Will contain the field and the error message",
        examples=[
            {
                "email": "An email address must have an @-sign.",
                "password": "Password should be at least 5 characters long",
            }
        ],
    )

    @classmethod
    def format_error_msg(self, msg):
        if ":" in msg:
            return msg.split(":")[-1].strip()
        if "," in msg:
            return msg.split(",")[-1].strip()

        return msg

    @staticmethod
    def format(errors):
        validation = {}
        for error in errors:
            if len(error["loc"]) == 1:
                validation["payload"] = "Payload is required"
                continue

            field = error["loc"][1]
            validation[field] = ValidationErrorResponseSchema.format_error_msg(
                error["msg"]
            )

        return ValidationErrorResponseSchema(
            uuid=str(uuid.uuid4()),
            message="Validation error",
            validation=validation,
        )
