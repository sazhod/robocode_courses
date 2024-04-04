from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from course.viewsets.moderator import ModeratorViewSet
from course.viewsets.methodist import MethodistViewSet


router = DefaultRouter()
# router.register(r'', UpgradeUserViewSet, basename='upgrade')

urlpatterns = [
    path('', ModeratorViewSet.as_view({'post': 'create_course'})),
    path('<int:pk>', ModeratorViewSet.as_view({'patch': 'update_course'})),
    path('<int:course_pk>/module', MethodistViewSet.as_view({'post': 'create_module'})),
    path('<int:course_pk>/module/<int:pk>', MethodistViewSet.as_view({'patch': 'update_module'})),

]

# urlpatterns += router.urls
# print(urlpatterns)
