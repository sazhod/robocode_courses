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
from django.db.utils import IntegrityError


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

    def get_filter_params(self, request, course_pk: int = None, serial_number: int = None) -> dict:
        """
        Метод формирующий dict параметров для выборки модулей.
        Если запрос отправляет методист или модератор, в выборку будут включены ещё не опубликованные модули.
        """
        filter_params = dict()

        if course_pk is not None:
            filter_params['course__pk'] = course_pk
        if serial_number is not None:
            filter_params['serial_number'] = serial_number
        if not is_moderator_or_methodist(request=request, view=self):
            filter_params['is_published'] = True

        return filter_params

    def get_object_or_400(self, request, course_pk, serial_number) -> Module | Response:
        """
        Метод получения модуля по id курса и номеру модуля.
        Если модуль не найден возвращается Response().
        """
        response: dict = get_default_response()

        try:
            filter_params = self.get_filter_params(request, course_pk, serial_number)
            instance = Module.objects.get(**filter_params)
            return instance
        except Module.DoesNotExist:
            response.update({
                'error': f'Модуль под номером {serial_number} в курсе {course_pk} не найден.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, course_pk: int):
        """
        Endpoint courses/{id}/modules/
        method GET
        Отвечает за получение списка модулей в выбранном курсе.
        """
        response: dict = get_default_response()
        request.data['course'] = course_pk

        filter_params = self.get_filter_params(request, course_pk)
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
        if (instance := self.get_object_or_400(request, course_pk, serial_number)) and isinstance(instance, Response):
            return instance

        serializer = ModuleSerializer(instance=instance)

        response: dict = get_default_response()
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
        response: dict = get_default_response()
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            response.update({
                'error': f'Курс {course_pk} не найден.',
            })
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateModuleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['course'] = course
            try:
                serializer.save()
            except IntegrityError:
                response.update({
                    'error': f'В курсе {course_pk} уже существует модуль под номером '
                             f'{serializer.validated_data["serial_number"]}.',
                })
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            response.update({
                'message': 'Модуль успешно добавлен.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_201_CREATED)

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

        if (instance := self.get_object_or_400(request, course_pk, serial_number)) and isinstance(instance, Response):
            return instance

        response: dict = get_default_response()

        serializer = CreateModuleSerializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response.update({
                'message': 'Модуль успешно обновлен.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_200_OK)

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

        if (instance := self.get_object_or_400(request, course_pk, serial_number)) and isinstance(instance, Response):
            return instance

        self.perform_destroy(instance)

        response: dict = get_default_response()
        response.update({
            'message': f'Модуль под номером {serial_number} в курсе {course_pk} был успешно удален.'
        })

        return Response(response, status=status.HTTP_200_OK)

