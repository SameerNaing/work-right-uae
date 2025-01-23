import os
import dotenv

from celery import Celery
from celery.schedules import crontab


dotenv.load_dotenv()

celery_app = Celery(__name__)
print(os.getenv("REDIS_URL"))
celery_app.conf.broker_url = os.getenv("REDIS_URL")

celery_app.autodiscover_tasks(["app.tasks"], force=True)
celery_app.set_default()
