import asyncio
from celery import Task
from asgiref.sync import async_to_sync
from aioredis import Redis

from app.core.db import SyncSessionLocal
from app.core.redis import get_redis_client


class BaseTask(Task):
    def __init__(self):
        self.sessions = {}
        self.redis_sessions = {}

    def before_start(self, task_id, args, kwargs):
        self.sessions[task_id] = SyncSessionLocal()
        self.redis_sessions[task_id] = asyncio.run(get_redis_client())
        super().before_start(task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        session = self.sessions.pop(task_id)
        session.close()

        super().on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        session = self.sessions.pop(task_id)
        session.close()

        super().after_return(status, retval, task_id, args, kwargs, einfo)

    @property
    def session(self):
        return self.sessions[self.request.id]

    @property
    def redis(self) -> Redis:
        return self.redis_sessions[self.request.id]
