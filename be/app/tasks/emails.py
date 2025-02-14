import time
from celery import shared_task

from app.engines import mailer_engine


from app.scrapers.mohre_scraper import get_mohre_services_urls


@shared_task(
    name="send_email",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 5, "countdown": 4},
)
def send_email(to, subject, body):
    mailer_engine.send_mail(to, subject, body)
