from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.db.session import get_db
from app.models.documents import DocumentModel
from app.core.config import settings
from app.tasks.uae_site_tasks import download_mohre_docs


router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
)


@router.get("/login", summary="Login", description="Endpoint for login")
async def login(db: AsyncSession = Depends(get_db)):
    download_mohre_docs.delay()
    return {"message": "Login"}


@router.get("/logout")
async def logout():
    pass
