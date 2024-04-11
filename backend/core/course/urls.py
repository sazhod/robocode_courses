from django.urls import path
from rest_framework.routers import SimpleRouter
from course.viewsets.course import CourseViewSet
from course.viewsets.module import ModuleViewSet
from course.viewsets.lesson import LessonViewSet


router = SimpleRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'modules', ModuleViewSet, basename='modules')


urlpatterns = [
    path('modules/<int:module_pk>/lessons', LessonViewSet.as_view({'post': 'create_lesson'})),
    path('modules/<int:module_pk>/lessons/<int:pk>', LessonViewSet.as_view({'patch': 'update_lesson'})),

]

urlpatterns += router.urls

