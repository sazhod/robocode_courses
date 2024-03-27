from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.course import Course
from ..serializers import CourseSerializer
from common.permissions import IsModerator


User = get_user_model()


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # authentication_classes = []
    # permission_classes = []

    # Не работает вместе авторизацией по JWT
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create_course':
            permission_classes.append(IsModerator)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_course(self, request):
        """
        Эндпоинт для добавления новых курсов модератором
        """

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['moderator'] = request.user
            serializer.save()
            return Response(serializer.data)

