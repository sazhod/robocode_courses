from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Пользовательский UserManager для создания и сохранения User и SuperUser.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Создание и сохранение пользователя.
        """
        if not email:
            raise ValueError("Email не указан.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Установка флагов для user.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Установка флагов для superuser.
        """
        extra_fields.setdefault('role', settings.SUPERUSER)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class TeacherManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=settings.TEACHER)


class StudentManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=settings.STUDENT)


class UndefinedUserManager(CustomUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=settings.UNDEFINED)
