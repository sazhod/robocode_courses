from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .viewsets.moderator import ModeratorViewSet


router = DefaultRouter()
# router.register(r'', UpgradeUserViewSet, basename='upgrade')

urlpatterns = [
    path('create', ModeratorViewSet.as_view({'post': 'create_course'})),
    path('<int:pk>/update', ModeratorViewSet.as_view({'patch': 'update_course'})),
]

# urlpatterns += router.urls
# print(urlpatterns)
