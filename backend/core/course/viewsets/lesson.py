from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.lesson import Lesson
from ..serializers import CreateLessonSerializer
from common.permissions import IsMethodist
from common.constants import get_default_response


User = get_user_model()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = CreateLessonSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create_lesson', 'update_lesson']:
            permission_classes.append(IsMethodist)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_lesson(self, request, module_pk: int):
        """
        Endpoint modules/{id}/lessons/
        method POST
        Отвечает за добавление нового урока в модуль методистом
        """
        request.data['course'] = module_pk
        serializer = CreateLessonSerializer(data=request.data)

        response: dict = get_default_response()
        if serializer.is_valid():
            serializer.save()
            response.update({
                'message': 'Урок успешно добавлен.',
                'data': serializer.data
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

        response.update({
            'error': serializer.errors
        })
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def update_lesson(self, request, module_pk: int, pk=None):
        """
        Endpoint modules/{id}/lessons/{id}
        method PATCH
        Отвечает за обновление информации об уроке методистом
        """
        instance = self.get_object()
        serializer = CreateLessonSerializer(instance=instance, data=request.data, partial=True)

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

    @action(detail=False, methods=['get'])
    def get_pdf(self):
        pass

