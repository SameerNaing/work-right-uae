import os
import dotenv

from celery import Celery
from celery.schedules import crontab


dotenv.load_dotenv()


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
result_backend = redis_url + "/1"
broker_url = redis_url + "/0"

celery_app = Celery(__name__)
celery_app.conf.broker_url = broker_url
celery_app.autodiscover_tasks(["app.tasks"], force=True)
celery_app.set_default()
