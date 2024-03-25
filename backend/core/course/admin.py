from django.contrib import admin
from .models.course import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass

