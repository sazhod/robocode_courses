from rest_framework import routers, status
from django.urls import reverse
from rest_framework.test import APITestCase
from ..models.module import Module
from ..models.course import Course
from ..serializers import ModuleSerializer, CreateModuleSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class ModuleViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        """
        Установка тестовых данных.
        """
        self.moderator = User.objects.create_user(
            email='test_moderator@moderator.ru',
            password='test_moderator_qazwsxedc123',
            role=5,
            phone_number='+7 (001) 999-99-99'
        )
        self.methodist = User.objects.create_user(
            email='test_methodist@moderator.ru',
            password='test_methodist_qazwsxedc123',
            role=6,
            phone_number='+7 (002) 999-99-99'
        )
        self.user = User.objects.create_user(
            email='test_user@user.ru',
            password='test_user_qazwsxedc123',
            role=3,
            phone_number='+7 (003) 999-99-99'
        )
        self.client.force_authenticate(user=self.methodist)

        self.course = Course.objects.create(
            start_date='2024-04-18',
            cost=100,
            moderator=self.moderator,
            methodist=self.methodist,
            is_published=False
        )
        self.first_module_published = Module.objects.create(
            title='first module',
            description='first module',
            serial_number=1,
            course=self.course,
            is_published=True
        )
        self.second_module_unpublished = Module.objects.create(
            title='second module',
            description='second module',
            serial_number=2,
            course=self.course
        )
        self.modules = [self.first_module_published, self.second_module_unpublished]

    def test_get_queryset_authenticated_methodist(self):
        url = reverse('modules-list', args=(self.course.pk,))

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        response_module_data = response.data.get('data')

        serializer = ModuleSerializer(self.modules, many=True)
        self.assertEquals(serializer.data, response_module_data)

    def test_get_queryset_unauthenticated_user(self):
        self.client.logout()
        url = reverse('modules-list', args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_queryset_authenticated_user(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user)

        url = reverse('modules-list', args=(self.course.pk,))

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))
        response_module_data = response.data.get('data')

        serializer = ModuleSerializer([self.first_module_published], many=True)
        self.assertEquals(serializer.data, response_module_data)

    def test_retrieve_module(self):
        url = reverse('modules-detail', args=(self.course.pk, self.first_module_published.pk))
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        serializer = ModuleSerializer(self.first_module_published)
        response_module_data = response.data.get('data')
        self.assertEquals(serializer.data, response_module_data)

    def test_create_module_with_correct_serial_number(self):
        url = reverse('modules-list', args=(self.course.pk, ))

        data = {
            'title': 'second module',
            'description': 'second module',
            'serial_number': 3
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
