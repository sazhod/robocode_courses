from django.conf import settings


LIMIT_CHOICE_TO = {
    'moderator': [
        settings.MODERATOR,
        settings.SUPERUSER
    ],
    'methodist': [
        settings.METHODIST,
        settings.SUPERUSER
    ]
}

DEFAULT_RESPONSE = {
    'error': None,
    'message': None,
    'data': None
}


def get_default_response():
    return DEFAULT_RESPONSE.copy()

