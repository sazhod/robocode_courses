from django.urls import path, include
from rest_framework.routers import SimpleRouter
from course.viewsets.course import CourseViewSet
from course.viewsets.module import ModuleViewSet
from course.viewsets.lesson import LessonViewSet


courses_router = SimpleRouter()
courses_router.register(r'courses', CourseViewSet, basename='courses')

# modules_router = SimpleRouter()
# modules_router.register(r'/modules', ModuleViewSet, basename='modules')


urlpatterns = [
    path('modules/<int:module_pk>/lessons', LessonViewSet.as_view({'post': 'create_lesson'})),
    path('modules/<int:module_pk>/lessons/<int:pk>', LessonViewSet.as_view({'patch': 'update_lesson'})),

    path('', include(courses_router.urls)),
    path('courses/<int:course_pk>/modules', ModuleViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='modules-list'),
    path('courses/<int:course_pk>/modules/<int:serial_number>',
         ModuleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='modules-detail'),
]
# print(router.urls)
# urlpatterns += router.urls

