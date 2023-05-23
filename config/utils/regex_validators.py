import re
from collections import namedtuple

from django.conf import settings

from rest_framework import serializers


def check_username(value):
    if not re.match(settings.USERNAME_REGEX, value):
        raise serializers.ValidationError(detail=f"{value} is in incorrect format")


def check_password(value):
    if not re.match(settings.PASSWORD_REGEX, value):
        raise serializers.ValidationError(detail=f"{value} is in incorrect format")


def check_phone(value):
    if not re.match(settings.PHONE_REGEX, value):
        raise serializers.ValidationError(detail=f"{value} is in incorrect format")


Validators = namedtuple("validators", ("username", "password", "phone"))

validators = Validators(check_username, check_password, check_phone)
