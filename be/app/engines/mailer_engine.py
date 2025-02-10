import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


def send_mail(to: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = settings.MAILER_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(settings.MAILER_HOST, settings.MAILER_PORT)
    server.starttls()
    server.login(settings.MAILER_USER, settings.MAILER_PASSWORD)
    server.sendmail(settings.MAILER_USER, to, msg.as_string())
    server.quit()
