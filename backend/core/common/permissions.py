from rest_framework.permissions import BasePermission
from django.conf import settings


class ModeratorPermission(BasePermission):
    message = "Доступ запрещен."

    def has_permission(self, request, view):
        if request.type in ['GET', 'POST']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == settings.MODERATOR:
            return True
        if request.user.is_superuser:
            return True
        return False
