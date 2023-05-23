from django.core.mail import send_mail
from django.conf import settings

from typing import List

from notifications.models import Email


def send_email(subject: str, message: str, recipients: List[str], from_email: str = settings.EMAIL_HOST):
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipients)

    Email.objects.bulk_create(
        [Email(
            from_email=from_email, to_email=recipient, subject=subject, message=message) for recipient in recipients]
    )
