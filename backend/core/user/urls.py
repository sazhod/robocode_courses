from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (AllUsersListAPIView, TeachersListAPIView, StudentsListAPIView,
                    UndefinedUsersListAPIView, UserRetrieveAPIView, RegistrationAPIView)
from .viewset import (UpgradeUserViewSet,)

router = DefaultRouter()
# router.register(r'', UpgradeUserViewSet, basename='upgrade')

urlpatterns = [
    # path('', AllUsersListAPIView.as_view()),
    path('teachers/', TeachersListAPIView.as_view()),
    path('students/', StudentsListAPIView.as_view()),
    path('undefined/', UndefinedUsersListAPIView.as_view()),
    # path('<int:pk>/', UserRetrieveAPIView.as_view()),
    # path('registration/', RegistrationAPIView.as_view()),
    path('<int:pk>/upgrade/to_moderator', UpgradeUserViewSet.as_view({'patch': 'to_moderator'})),
    path('<int:pk>/upgrade/to_methodist', UpgradeUserViewSet.as_view({'patch': 'to_methodist'})),
]

# urlpatterns += router.urls
# print(urlpatterns)
