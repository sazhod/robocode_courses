from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from ..models.course import Course
from ..serializers import CourseSerializer
from common.permissions import ModeratorPermission


User = get_user_model()


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=False, methods=['get'], permission_classes=[ModeratorPermission])
    def create_course(self, request):
        """
        Эндпоинт для добавления новых курсов модератором
        """

        # Поправить логику создания
        # Не проверяется дата курса
        # Включить request.user как moderator
        result = CourseSerializer(data=request.data, many=False)
        if not result.is_valid():
            return Response(result.data)

        result.save()
        return Response(result.data)
