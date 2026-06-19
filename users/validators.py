import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

PHONE_LENGTH_WITH_PREFIX_8 = 11
PHONE_DIGITS_COUNT = 10

PHONE_PATTERN = re.compile(rf"^(8|\+7)\d{{{PHONE_DIGITS_COUNT}}}$")


def normalize_phone(phone):
    phone = phone.strip()
    if phone.startswith("8") and len(phone) == PHONE_LENGTH_WITH_PREFIX_8:
        return "+7" + phone[1:]
    return phone


def validate_phone(value):
    if not PHONE_PATTERN.match(value):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )


def validate_github_url(value):
    if not value:
        return
    validator = URLValidator()
    validator(value)
    if "github.com" not in value.lower():
        raise ValidationError("Ссылка должна вести на GitHub")
