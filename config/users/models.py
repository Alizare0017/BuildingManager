from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.conf import settings


class User(AbstractUser):
    MANAGER = "MANAGER"
    RESIDENT = "RESIDENT"
    role_choices = (
        (MANAGER, "manager"),
        (RESIDENT, "resident")
    )
    phone = models.CharField(
        max_length=13, validators=[RegexValidator(regex=settings.PHONE_REGEX)], null=True, blank=True
    )
    role = models.CharField(max_length=8, choices=role_choices, null=True, blank=True)

    is_phone_activated = models.BooleanField(default=False)
    is_email_activated = models.BooleanField(default=False)

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_resident(self):
        return self.role == self.RESIDENT

    @property
    def full_name(self):
        return self.first_name + self.last_name

