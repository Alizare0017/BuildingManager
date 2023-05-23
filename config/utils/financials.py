from django.utils import timezone

from rest_framework.serializers import ValidationError


def get_expire_date(data):
    return timezone.now() + timezone.timedelta(days=data["expire_date"])


def check_serializer_keys(data):
    if not data.get("unit") and not data.get("divide_by"):
        raise ValidationError("specific unit or division method must be provided")
    if data.get("unit") and data.get("divide_by"):
        raise ValidationError("only a specific unit or a division method must be provided")
    return data
