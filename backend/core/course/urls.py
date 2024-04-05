from django.urls import path
from rest_framework.routers import DefaultRouter
from course.viewsets.course import CourseViewSet
from course.viewsets.module import ModuleViewSet
from course.viewsets.lesson import LessonViewSet


urlpatterns = [
    path('courses', CourseViewSet.as_view({'post': 'create_course'})),
    path('courses/<int:pk>', CourseViewSet.as_view({'patch': 'update_course'})),
    path('courses/<int:course_pk>/modules', ModuleViewSet.as_view({'post': 'create_module'})),
    path('courses/<int:course_pk>/modules/<int:pk>', ModuleViewSet.as_view({'patch': 'update_module'})),
    path('modules/<int:module_pk>/lessons', LessonViewSet.as_view({'post': 'create_lesson'})),
    path('modules/<int:module_pk>/lessons/<int:pk>', LessonViewSet.as_view({'patch': 'update_lesson'})),
]

