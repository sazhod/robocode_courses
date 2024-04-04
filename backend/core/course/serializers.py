from importlib._bootstrap import _spec_from_module

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.course import Course
from user.serializers import CustomUserSerializer
from django.utils import timezone
from .models.module import Module


User = get_user_model()


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        abstract = True

    def validate(self, attrs):
        if attrs['start_date'] is None:
            raise serializers.ValidationError('Дата начала не должна быть пустой!')
        if attrs['start_date'] <= timezone.localdate():
            raise serializers.ValidationError('Дата начала должна быть позже текущей даты!')
        return attrs


class CreateCourseSerializer(BaseCourseSerializer):
    moderator = CustomUserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('start_date', 'cost', 'methodist', 'moderator')


class UpdateCourseSerializer(BaseCourseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, attrs):
        if 'start_date' not in attrs:
            return attrs
        return super().validate(attrs)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class CreateModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('course', 'title', 'description', 'serial_number')

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'role')
#         extra_kwargs = {"password": {"write_only": True}}
#
#     # def create(self, validated_data):
#     #     user = CustomUser.objects.create_user(**validated_data)
#     #     return user
#
#
# class RegistrationSerializer(serializers.ModelSerializer):
#     """ Сериализация регистрации пользователя и создания нового. """
#
#     password = serializers.CharField(
#         max_length=128,
#         min_length=8,
#         write_only=True
#     )
#
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'last_name', 'first_name', 'patronymic', 'phone_number', 'token')
#         extra_kwargs = {"password": {"write_only": True}}
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
