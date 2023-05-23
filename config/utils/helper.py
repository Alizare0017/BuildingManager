import random
import string

from django.contrib.auth.hashers import make_password
from django.utils import timezone


def _generate_random_number(length) -> int:
    numbers = list(string.digits)
    number = str()
    for _ in range(length):
        number += random.choice(numbers)
    return int(number)


def _generate_random_letters(length) -> str:
    letters = str()
    for _ in range(length):
        letters += random.choice(list(string.ascii_letters))
    return letters


def random_username(building):
    return f"{building.name}_user_{_generate_random_number(5)}{_generate_random_letters(2)}"


def generate_random_password(length, hashed=False):
    random_numbers = list(str(_generate_random_number(50)))
    random_letters = list(_generate_random_letters(20))
    rand_chars = random_letters + random_numbers
    password = str()
    for _ in range(length):
        password += random.choice(rand_chars)
    if hashed:
        return make_password(password=password)
    return password


def generate_otp():
    return _generate_random_number(6)


def generate_otp_expire_date():
    return timezone.now() + timezone.timedelta(seconds=60)


