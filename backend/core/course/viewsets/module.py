from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.module import Module, Course
from ..serializers import ModuleSerializer, CreateModuleSerializer
from common.permissions import IsMethodist
from common.constants import get_default_response


User = get_user_model()


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        # if self.action in ['create_module', 'update_module']:
        #     permission_classes.append(IsMethodist)
        return [permission() for permission in permission_classes]

    def list(self, request, course_pk: int):
        """
        Endpoint courses/{id}/modules/
        method GET
        Отвечает за получение списка модулей в выбранном курсе.
        """
        response: dict = get_default_response()
        request.data['course'] = course_pk
        modules = Module.objects.filter(course__pk=course_pk)
        if not modules:
            response.update({
                'error': f'Модули не найдены.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ModuleSerializer(data=modules, many=True)
        response: dict = get_default_response()
        serializer.is_valid()

        response.update({
            'message': f'Список модулей курса {course_pk}.',
            'data': serializer.data
        })
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, course_pk: int):
        """
        Endpoint courses/{id}/modules/
        method POST
        Отвечает за добавление нового модуля в курс методистом
        """
        request.data['course'] = course_pk
        serializer = CreateModuleSerializer(data=request.data)

        response: dict = get_default_response()
        if serializer.is_valid():
            serializer.save()
            response.update({
                'message': 'Модуль успешно добавлен.',
                'data': serializer.data
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

        response.update({
            'error': serializer.errors
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, course_pk: int, pk=None):
        return self.partial_update(request, course_pk, pk)

    def partial_update(self, request, course_pk: int, pk=None):
        """
        Endpoint course/{id}/module/{id}
        method PATCH
        Отвечает за обновление информации о модуле методистом
        """
        instance = self.get_object()
        serializer = CreateModuleSerializer(instance=instance, data=request.data, partial=True)

        response: dict = get_default_response()
        if serializer.is_valid():
            serializer.save()
            response.update({
                'message': 'Модуль успешно обновлен.',
                'data': serializer.data
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

        response.update({
            'error': serializer.errors
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
