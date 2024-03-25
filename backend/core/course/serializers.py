from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.course import Course


User = get_user_model()


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('start_date', 'cost', 'methodist')


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
