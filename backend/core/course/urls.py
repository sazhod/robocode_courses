from django.urls import path
from rest_framework.routers import DefaultRouter
from course.viewsets.course import CourseViewSet
from course.viewsets.module import ModuleViewSet


urlpatterns = [
    path('', CourseViewSet.as_view({'post': 'create_course'})),
    path('<int:pk>', CourseViewSet.as_view({'patch': 'update_course'})),
    path('<int:course_pk>/module', ModuleViewSet.as_view({'post': 'create_module'})),
    path('<int:course_pk>/module/<int:pk>', ModuleViewSet.as_view({'patch': 'update_module'})),
]

