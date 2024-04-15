from django.contrib.auth import get_user_model
from django.db import models


class TitleDescMixin(models.Model):
    """
        Mixin содержащий поля название и описание
    """
    title = models.CharField(verbose_name='Название', max_length=255, blank=True, null=True, default='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True, default='Описание')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title}({self.pk})'


class TimestampMixin(models.Model):
    """
        Mixin содержащий поля время создания и время обновления
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
