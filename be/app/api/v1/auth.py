from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from app.db.session import get_db
from app.models.documents import DocumentModel

router = APIRouter(
    prefix="/v1/auth",
    tags=["Auth"],
)


@router.get("/login", summary="Login", description="Endpoint for login")
async def login(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DocumentModel))
    documents = result.scalars().all()
    for i in documents:
        print(i.id, i.text)

    return {"message": "Login"}
