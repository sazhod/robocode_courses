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


