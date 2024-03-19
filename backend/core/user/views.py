from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from .serializers import CustomUserSerializer, RegistrationSerializer

User = get_user_model()


class RegistrationAPIView(APIView):
    """
    Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
    """
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        print(user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllUsersListAPIView(generics.ListAPIView):
    queryset = User.objects.all().exclude(role=settings.SUPERUSER)
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class TeachersListAPIView(generics.ListAPIView):
    queryset = User.teachers.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class StudentsListAPIView(generics.ListAPIView):
    queryset = User.students.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class UndefinedUsersListAPIView(generics.ListAPIView):
    queryset = User.undefined_users.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(User.objects, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

