from rest_framework.permissions import BasePermission
from django.conf import settings


class IsModerator(BasePermission):
    message = "Доступ запрещен."

    def has_permission(self, request, view):
        print(request.user)
        return request.user.is_authenticated and (request.user.role == settings.MODERATOR or request.user.is_superuser)


