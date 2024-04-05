from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.course import Course
from ..serializers import CreateCourseSerializer, UpdateCourseSerializer
from common.permissions import IsModerator
from common.constants import get_default_response


User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CreateCourseSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create_course', 'update_course']:
            permission_classes.append(IsModerator)
        return [permission() for permission in permission_classes]

    def post(self):
        pass

    @action(detail=False, methods=['post'])
    def create_course(self, request):
        """
        Endpoint course/create
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

    @action(detail=True, methods=['patch'])
    def update_course(self, request, pk=None):
        """
        Endpoint course/<int:pk>/update
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

