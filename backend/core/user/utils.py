from django.db.models import Count, F, Value, Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .serializers import CustomUserSerializer
from common.constants import get_default_response
User = get_user_model()


def upgrade_undefined_user_role(pk: int, role: int) -> Response:
    response: dict = get_default_response()

    try:
        user = User.undefined_users.get(pk=pk)
    except ObjectDoesNotExist:
        response.update({
            'error': 'Пользователь не найден'
        })
        return Response(response,
                        status=status.HTTP_400_BAD_REQUEST)
    user.role = role
    user.is_staff = True
    user.save()
    serializer = CustomUserSerializer(instance=user)
    response.update({
        'message': f'Пользователь "{user.email}" получил права "{user.get_role_display()}(а)".',
        'data': serializer.data
    })
    return Response(response, status=status.HTTP_200_OK)
