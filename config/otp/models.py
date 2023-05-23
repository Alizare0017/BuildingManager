from django.db import models
from django.utils import timezone
from django.conf import settings

from utils.helper import generate_otp, generate_otp_expire_date
from users.models import User


class OTPManager(models.Manager):
    def get_or_create(self, user, **kwargs):
        otp = self.filter(user=user).last()
        if not otp or otp.is_expired:
            return self.create(user=user, **kwargs)
        return otp


class OTP(models.Model):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    type_choices = [
        (EMAIL, "email"),
        (PHONE, "sms")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.IntegerField(default=generate_otp)
    expire_date = models.DateTimeField(default=generate_otp_expire_date)
    otp_for = models.CharField(max_length=5, choices=type_choices)
    used = models.BooleanField(default=False)

    objects = OTPManager()

    @property
    def is_expired(self):
        return self.expire_date < timezone.now()

    def burn(self):
        self.used = True
        self.save()