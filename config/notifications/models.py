from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Email(models.Model):
    from_email = models.EmailField()
    to_email = models.EmailField()
    subject = models.CharField(max_length=225)
    message = models.TextField()


class SMS(models.Model):
    from_number = models.CharField(max_length=20)
    to_number = models.CharField(max_length=13, validators=[RegexValidator(settings.PHONE_REGEX)])
    message = models.TextField()
