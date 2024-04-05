from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from common.models.mixins import TitleDescMixin, TimestampMixin
from common.constants import LIMIT_CHOICE_TO
from django.core.exceptions import ValidationError
from django.utils import timezone
from .module import Module


User = get_user_model()


class Lesson(TitleDescMixin, TimestampMixin, models.Model):
    """
        Модель описывающая урок.
    """
    pdf_material = models.FileField(verbose_name='Материал', upload_to='pdf')
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
