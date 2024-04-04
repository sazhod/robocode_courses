from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from common.models.mixins import TitleDescMixin, TimestampMixin
from django.utils import timezone
from ..models.course import Course
from django.core.validators import MinValueValidator


User = get_user_model()


class Module(TitleDescMixin, TimestampMixin, models.Model):
    """
        Модель описывающая модуль в курсе
    """
    serial_number = models.PositiveSmallIntegerField(verbose_name='Порядковый номер', validators=[MinValueValidator(1)])

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE,
                               related_name='course')
    is_published = models.BooleanField(verbose_name='Опубликован?', default=False)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'

        constraints = [
            models.UniqueConstraint(
                fields=("serial_number", "course"), name="unique_serial_number_in_course"
            ),
        ]
