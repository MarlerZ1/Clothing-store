import uuid

from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta

from users.models import EmailVerification, User


@shared_task(bind=True, default_retry_delay=60)
def send_email_verification(self, user_id):
    try:
        user = User.objects.get(id=user_id)
        expiration = now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
    except Exception as exc:
        raise self.retry(exc=exc)