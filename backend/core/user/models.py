from django.contrib.auth.models import User, AbstractUser
from django.db import models
from .managers import CustomUserManager, TeacherManager, StudentManager, UndefinedUserManager
from django.conf import settings
from django.core.validators import RegexValidator
from datetime import datetime, timedelta


class CustomUser(AbstractUser):
    """
    Пользовательская модель User с авторизацией по полям email и password
    """
    username = None
    email = models.EmailField("email адрес", unique=True)
    role = models.PositiveSmallIntegerField(verbose_name='Роль',
                                            choices=settings.USER_ROLE_CHOICES, default=settings.STUDENT)

    patronymic = models.CharField(verbose_name='Отчество', max_length=150, blank=True)
    phone_regex = RegexValidator(regex=r'^(\+7)\s?\(?[489][0-9]{2}\)\s?[0-9]{3}\-[0-9]{2}\-[0-9]{2}$',
                                 message="Телефон должен иметь 18 символов и следующий формат: '+7 (999) 999-99-99'.")
    phone_number = models.CharField(verbose_name='Номер телефона', validators=[phone_regex],
                                    max_length=18, blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number', 'last_name', 'first_name', 'patronymic']

    objects = CustomUserManager()
    teachers = TeacherManager()
    students = StudentManager()
    undefined_users = UndefinedUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{str(self.last_name).capitalize()} " \
               f"{str(self.first_name).capitalize()} " \
               f"{str(self.patronymic).capitalize()}".strip()

    def get_short_name(self):
        return f"{str(self.last_name).capitalize()} " \
               f"{str(self.first_name).capitalize()} ".strip()


