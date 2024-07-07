from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from store_server.settings import DOMAIN_NAME, EMAIL_HOST_USER


# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email_verification', args=(self.user.email, self.code))
        verification_link = DOMAIN_NAME + link

        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи для {self.user.email} перейдите по ссылке: {verification_link} '

        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False
        )

    def is_expired(self):
        return now() >= self.expiration
