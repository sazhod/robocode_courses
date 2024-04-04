from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.module import Module, Course
from ..serializers import ModuleSerializer, CreateModuleSerializer
from common.permissions import IsMethodist
from django.core import exceptions


User = get_user_model()


class MethodistViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create_module', 'update_module']:
            permission_classes.append(IsMethodist)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_module(self, request, course_pk: int):
        """
        Endpoint course/<int:pk>/module/create
        method POST
        Отвечает за добавление нового модуля в курс методистом
        """
        request.data['course'] = course_pk
        serializer = CreateModuleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_module(self, request, course_pk: int, pk=None):
        """
        Endpoint course/<int:pk>/update
        method PATCH
        Отвечает за обновление информации о модуле методистом
        """
        if pk is None:
            return Response({'status': 'Выберите модуль.'}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        serializer = CreateModuleSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
