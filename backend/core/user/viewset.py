from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import CustomUserSerializer
from .utils import upgrade_undefined_user_role


User = get_user_model()


class UpgradeUserViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet для модели User. В нем реализованы эндпоинты для обновления ролей нераспределенных пользователей.
    Энпоинты доступные только SuperUser.
    """
    queryset = User.undefined_users.all()
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def to_moderator(self, request, pk=None):
        """
        Endpoint users/{id}/upgrade/to_moderator
        method PATCH
        Отвечает за предоставление нераспределенному пользователю роли Moderator
        """
        return upgrade_undefined_user_role(pk, settings.MODERATOR)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdminUser])
    def to_methodist(self, request, pk=None):
        """
        Endpoint users/{id}/upgrade/to_methodist
        method PATCH
        Отвечает за предоставление нераспределенному пользователю роли Methodist
        """
        return upgrade_undefined_user_role(pk, settings.METHODIST)
