from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseFields(models.Model):
    """
        Класс в котором описаны общие поля и методы для всех моделей
    """
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Course(BaseFields):
    """
        Модель описывающая курс
    """
    image = models.ImageField(verbose_name='Изображение')

    start_date = models.DateField(verbose_name='Дата старта', null=True)
    start_time = models.TimeField(verbose_name='Время старта')
    cost = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(BaseFields):
    """
        Модель описывающая урок
    """
    pdf_material = models.FileField(verbose_name='Материал', upload_to='pdf')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Homework(BaseFields):
    """
        Модель описывающая Д/з
    """

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'


class LessonTeacherVideo(models.Model):
    """
        Модель описывающая записи занятий
    """
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE)
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE)
    video_link = models.URLField(verbose_name='Запись')

    class Meta:
        verbose_name = 'Запись занятия'
        verbose_name_plural = 'Записи занятий'

    def __str__(self):
        return self.video_link
