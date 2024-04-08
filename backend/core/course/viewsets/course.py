from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.course import Course
from ..serializers import CreateCourseSerializer, UpdateCourseSerializer, BaseCourseSerializer
from common.permissions import IsModerator, IsMethodist
from common.constants import get_default_response


User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CreateCourseSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes.append(IsModerator)
        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        Endpoint api/course/
        method GET
        Отвечает за получения списка курсов.
        Авторизованный модератор/методист/superuser получает список всех курсов.
        Остальные получают только опубликованные курсы.
        """
        if IsModerator().has_permission(request, self) or IsMethodist().has_permission(request, self):
            queryset = self.queryset
        else:
            queryset = Course.objects.filter(is_published=True)

        serializer = BaseCourseSerializer(data=queryset, many=True)
        serializer.is_valid()

        response: dict = get_default_response()
        if queryset:
            response.update({
                'message': 'Список курсов.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_200_OK)

        response.update({
            'error': 'Курсы не предоставлены.'
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        Endpoint api/course/{id}
        method GET
        Отвечает за получения информации о курсе.
        Авторизованный модератор/методист/superuser получает информации о любом курсе.
        Остальные получают только информацию об опубликованном курсе.
        """
        instance = self.get_object()
        response: dict = get_default_response()

        if ((IsModerator().has_permission(request, self) or IsMethodist().has_permission(request, self))
                or instance.is_published):
            serializer = BaseCourseSerializer(instance=instance)

            response.update({
                'message': 'Информация о выбранном курсе.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_200_OK)

        response.update({
            'error': 'Курс не найден.'
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        Endpoint api/course/
        method POST
        Отвечает за добавление нового курса модератором
        """
        response: dict = get_default_response()

        serializer = CreateCourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['moderator'] = request.user
            serializer.save()
            response.update({
                'message': 'Курс успешно добавлен.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_200_OK)

        response.update({
            'error': serializer.errors
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Endpoint api/course/{id}
        method PATCH
        Отвечает за обновление информации о курсе модератором
        """
        instance = self.get_object()
        serializer = UpdateCourseSerializer(instance=instance, data=request.data, partial=True)

        response: dict = get_default_response()

        if serializer.is_valid():
            serializer.save()
            response.update({
                'message': 'Курс успешно обновлен.',
                'data': serializer.data
            })
            return Response(response, status=status.HTTP_200_OK)

        response.update({
            'error': serializer.errors
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)

        response: dict = get_default_response()
        response.update({
            'message': 'Курс был успешно удален.'
        })

        return Response(response, status=status.HTTP_200_OK)