from rest_framework.permissions import BasePermission
from django.conf import settings


class IsModerator(BasePermission):
    message = "Доступ запрещен."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == settings.MODERATOR or request.user.is_superuser)


class IsMethodist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == settings.METHODIST or request.user.is_superuser)


def is_moderator_or_methodist(request, view):
    return IsModerator().has_permission(request, view) or IsMethodist().has_permission(request, view)

