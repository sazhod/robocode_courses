from django.db.models import Count, F, Value, Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


def upgrade_undefined_user_role(pk: int, role: int) -> Response:
    if pk is None:
        return Response({'status': f'Данные пользователя не предоставлены.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.undefined_users.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'status': f'Пользователь не найден.'},
                        status=status.HTTP_400_BAD_REQUEST)

    user.role = role
    user.is_staff = True
    user.save()

    return Response({'status': f'Пользователь "{user.email}" получил права "{user.get_role_display()}(а)".'},
                    status=status.HTTP_200_OK)
