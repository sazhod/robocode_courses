from rest_framework import permissions
from django.conf import settings


class IsSuperUserOnly(permissions.BasePermission):
    """
    CustomPermissions для доступа к статистике авторизованному пользователю с ролью учитель. ReadOnly.
    """
    edit_methods = ("GET",)

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role in (settings.TEACHER, settings.SUPERUSER):
            return True
        return False
