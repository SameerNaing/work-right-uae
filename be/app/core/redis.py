from aioredis import from_url

from app.core.config import settings 


redis_client = None


async def get_redis_client():
    return await from_url(settings.REDIS_URL)    



