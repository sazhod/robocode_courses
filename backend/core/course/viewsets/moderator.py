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

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create_course', 'update_course']:
            permission_classes.append(IsModerator)
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def create_course(self, request):
        """
        Endpoint course/create
        method POST
        Отвечает за добавление нового курса модератором
        """
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['moderator'] = request.user
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_course(self, request, pk=None):
        """
        Endpoint course/<int: pk>/update
        method POST
        Отвечает за обновление информации о курсе модератором
        """
        if pk is None:
            return Response({'status': 'Выберите курс.'}, status=status.HTTP_400_BAD_REQUEST)


