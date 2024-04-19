from rest_framework import routers, status
from django.urls import reverse
from rest_framework.test import APITestCase
from ..models.module import Module
from ..models.course import Course
from ..serializers import ModuleSerializer, CreateModuleSerializer
from django.contrib.auth import get_user_model
import datetime


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
            start_date=datetime.date.today() + datetime.timedelta(days=1),
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
        url = reverse('modules-detail', args=(self.course.pk, self.first_module_published.serial_number))
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
            'title': 'third module',
            'description': 'third module',
            'serial_number': 3
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))
        response_module_data = response.data.get('data')

        self.assertEquals(response_module_data.get('title'), data.get('title'))
        self.assertEquals(response_module_data.get('description'), data.get('description'))
        self.assertEquals(response_module_data.get('serial_number'), data.get('serial_number'))
        self.assertEquals(response_module_data.get('course'), self.course.pk)

    def test_create_module_with_existing_serial_number(self):
        url = reverse('modules-list', args=(self.course.pk, ))

        data = {
            'title': 'existing module',
            'description': 'existing module',
            'serial_number': 1
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIsNotNone(response.data.get('error'))

    def test_create_module_with_nonexistent_course(self):
        url = reverse('modules-list', args=(999,))

        data = {
            'title': 'third module',
            'description': 'third module',
            'serial_number': 3
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIsNotNone(response.data.get('error'))

    def test_update_module(self):
        url = reverse('modules-detail', args=(self.course.pk, self.second_module_unpublished.serial_number))
        data = {
            'title': 'Test title',
            'description': 'Test description',
            'serial_number': 3,
            'is_published': True
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))
        response_module_data = response.data.get('data')

        updated_module = Module.objects.get(course__pk=self.course.pk, pk=self.second_module_unpublished.pk)
        serializer = CreateModuleSerializer(updated_module)
        print(serializer.data, response_module_data)
        self.assertEquals(serializer.data, response_module_data)

    def test_partial_update_module(self):
        url = reverse('modules-detail', args=(self.course.pk, self.second_module_unpublished.serial_number))
        data = {
            'title': 'Test title(partial_update)'
        }
        response = self.client.patch(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))
        response_module_data = response.data.get('data')

        updated_module = Module.objects.get(course__pk=self.course.pk, pk=self.second_module_unpublished.pk)
        serializer = CreateModuleSerializer(updated_module)
        self.assertEquals(serializer.data, response_module_data)

    def test_destroy_module(self):
        url = reverse('modules-detail', args=(self.course.pk, self.second_module_unpublished.serial_number))
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('error', response.data)
        self.assertIsNone(response.data.get('error'))

        self.assertIn('message', response.data)
        self.assertIsNotNone(response.data.get('message'))
