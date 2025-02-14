from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.db.session import get_db
from app.core.config import settings
from app.services import user_service


router = APIRouter(
    prefix="/v1/profile",
    tags=["Profile"],
)


@router.get("/me", summary="Get logged in user profile")
async def get_me(db: AsyncSession = Depends(get_db)):
    return {"my": "profile"}


@router.patch("/me", summary="Update logged in user profile")
async def update_me():
    return {"my": "profile"}


@router.delete("/me", summary="Delete logged in user profile")
async def delete_me():
    return {"my": "profile"}
