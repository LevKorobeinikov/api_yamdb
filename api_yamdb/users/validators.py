import re

from django.core.exceptions import ValidationError

from api_yamdb.constants import CHECK_USERNAME, NO_USERNAMES


def validate_username(value):
    if value in NO_USERNAMES:
        raise ValidationError(
            'Использовать имя {value} в качестве username запрещено'
        )
    text = value
    pattern = re.compile(CHECK_USERNAME)
    match_obj = pattern.match(text)
    if match_obj is None:
        raise ValidationError(
            'В username использованы недопустимые символы'
        )
