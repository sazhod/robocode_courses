from rest_framework.permissions import BasePermission
from django.conf import settings


class IsModerator(BasePermission):
    message = "Доступ запрещен."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == settings.MODERATOR or request.user.is_superuser)


class IsMethodist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == settings.METHODIST or request.user.is_superuser)

