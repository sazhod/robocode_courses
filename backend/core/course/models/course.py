from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from common.models.mixins import TitleDescMixin, TimestampMixin
from common.constants import LIMIT_CHOICE_TO
from django.core.exceptions import ValidationError
from django.utils import timezone


User = get_user_model()


class Course(TitleDescMixin, TimestampMixin, models.Model):
    """
        Модель описывающая курс
    """
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    start_date = models.DateField(verbose_name='Дата старта')
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    moderator = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                  limit_choices_to=dict(role__in=LIMIT_CHOICE_TO['moderator']),
                                  related_name='moderator')
    methodist = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                  limit_choices_to=dict(role__in=LIMIT_CHOICE_TO['methodist']),
                                  related_name='methodist')
    is_published = models.BooleanField(verbose_name='Опубликован?', default=False)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def clean(self):
        """
        Метод валидации нового курса.
        Если указана прошедшая или текущая дата старта, то raise ValidationError.
        """
        super().clean()
        if self.start_date <= timezone.localdate():
            raise ValidationError('Дата начала должна быть позже текущей даты!')

# class Lesson(BaseFieldsMixin, models.Model):
#     """
#         Модель описывающая урок
#     """
#     pdf_material = models.FileField(verbose_name='Материал', upload_to='pdf')
#     course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name = 'Урок'
#         verbose_name_plural = 'Уроки'
#
#
# class Homework(BaseFieldsMixin, models.Model):
#     """
#         Модель описывающая Д/з
#     """
#
#     class Meta:
#         verbose_name = 'Домашнее задание'
#         verbose_name_plural = 'Домашние задания'
#
#
# class LessonTeacherVideo(models.Model):
#     """
#         Модель описывающая записи занятий
#     """
#     lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     video_link = models.URLField(verbose_name='Запись')
#
#     class Meta:
#         verbose_name = 'Запись занятия'
#         verbose_name_plural = 'Записи занятий'
#
#     def __str__(self):
#         return self.video_link

