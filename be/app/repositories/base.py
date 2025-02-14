from app.db.session import get_db


class BaseRepository:
    def __init__(self, db):
        self.db = db

    @classmethod
    async def instantiate(cls):
        db = await get_db().__anext__()
        return cls(db)
