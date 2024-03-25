from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from common.models.mixins import TitleDescMixin, TimestampMixin


User = get_user_model()


class Course(TitleDescMixin, TimestampMixin, models.Model):
    """
        Модель описывающая курс
    """
    image = models.ImageField(verbose_name='Изображение')
    start_date = models.DateField(verbose_name='Дата старта', null=True)
    start_time = models.TimeField(verbose_name='Время старта')
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    moderator = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                  limit_choices_to={'role': settings.MODERATOR}, related_name='moderator')
    methodist = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                  limit_choices_to={'role': settings.METHODIST}, related_name='methodist')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


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

