from django.contrib.auth import get_user_model
from django.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.module import Module, Course
from ..serializers import ModuleSerializer, CreateModuleSerializer
from common.permissions import IsMethodist, is_moderator_or_methodist
from common.constants import get_default_response



User = get_user_model()


@extend_schema_view(
    list=extend_schema(tags=['modules']),
    retrieve=extend_schema(tags=['modules']),
    create=extend_schema(tags=['modules']),
    update=extend_schema(tags=['modules']),
    partial_update=extend_schema(tags=['modules']),
)
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes.append(IsMethodist)
        return [permission() for permission in permission_classes]

    def list(self, request, course_pk: int):
        """
        Endpoint courses/{id}/modules/
        method GET
        Отвечает за получение списка модулей в выбранном курсе.
        """
        response: dict = get_default_response()
        request.data['course'] = course_pk
        filter_params = {
            'course__pk': course_pk
        }
        if not is_moderator_or_methodist(request=request, view=self):
            filter_params['is_published'] = True

        modules = Module.objects.filter(**filter_params)

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

    def retrieve(self, request, course_pk: int, serial_number: int):
        """
        Endpoint courses/{id}/modules/{serial_number}
        method GET
        Отвечает за получение информации о модуле в выбранном курсе.
        """
        response: dict = get_default_response()

        try:
            filter_params = {
                'course__pk': course_pk,
                'serial_number': serial_number,
            }
            if not is_moderator_or_methodist(request=request, view=self):
                filter_params['is_published'] = True
            instance = Module.objects.get(**filter_params)
        except Module.DoesNotExist:
            response.update({
                'error': f'Модуль под номером {serial_number} в курсе {course_pk} не найден.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ModuleSerializer(instance=instance)

        response.update({
            'message': f'Информация о выбранном модуле курса {course_pk}',
            'data': serializer.data
        })
        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, course_pk: int):
        """
        Endpoint courses/{id}/modules/
        method POST
        Отвечает за добавление нового модуля в курс методистом.
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

    def update(self, request, course_pk: int, serial_number: int):
        """
        Endpoint courses/{id}/modules/{serial_number}
        method PUT
        Отвечает за полное обновление информации о модуле в выбранном курсе методистом.
        """
        return self.partial_update(request, course_pk, serial_number)

    def partial_update(self, request, course_pk: int, serial_number: int):
        """
        Endpoint course/{id}/module/{serial_number}
        method PATCH
        Отвечает за частичное обновление информации о модуле в выбранном курсе методистом.
        """
        response: dict = get_default_response()

        try:
            instance = Module.objects.get(course__pk=course_pk, serial_number=serial_number)
        except Module.DoesNotExist:
            response.update({
                'error': f'Модуль под номером {serial_number} в курсе {course_pk} не найден.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateModuleSerializer(instance=instance, data=request.data, partial=True)

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

    def destroy(self, request, course_pk: int, serial_number: int):
        """
        Endpoint course/{id}/module/{serial_number}
        method DELETE
        Отвечает за удаление модуля в выбранном курсе методистом.
        """
        response: dict = get_default_response()

        try:
            instance = Module.objects.get(course__pk=course_pk, serial_number=serial_number)
        except Module.DoesNotExist:
            response.update({
                'error': f'Модуль под номером {serial_number} в курсе {course_pk} не найден.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)

        response.update({
            'message': f'Модуль под номером {serial_number} в курсе {course_pk} был успешно удален.'
        })

        return Response(response, status=status.HTTP_200_OK)

