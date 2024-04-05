from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.course import Course
from user.serializers import CustomUserSerializer
from django.utils import timezone
from .models.module import Module
from .models.lesson import Lesson


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


class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
