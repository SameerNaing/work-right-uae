from celery import Task
from app.db.session import SessionLocal


class BaseTask(Task):
    def __init__(self):
        self.sessions = {}

    def before_start(self, task_id, args, kwargs):
        self.sessions[task_id] = SessionLocal()
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
        print("SESSION FROM BASETASK", self.sessions)
        return self.sessions[self.request.id]
