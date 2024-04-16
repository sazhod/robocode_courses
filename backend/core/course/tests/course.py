from rest_framework import routers, status
from django.urls import reverse
from rest_framework.test import APITestCase
from ..models.course import Course
from ..serializers import BaseCourseSerializer, CreateCourseSerializer, UpdateCourseSerializer
from django.contrib.auth import get_user_model
import datetime


User = get_user_model()


class CourseViewSetTestCase(APITestCase):
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
        self.client.force_authenticate(user=self.moderator)

        self.methodist = User.objects.create_user(
            email='test_methodist@moderator.ru',
            password='test_methodist_qazwsxedc123',
            role=6,
            phone_number='+7 (002) 999-99-99'
        )
        self.course_unpublished = Course.objects.create(
            start_date=datetime.date.today() + datetime.timedelta(days=1),
            cost=100,
            moderator=self.moderator,
            methodist=self.methodist,
            is_published=False
        )
        self.course_published = Course.objects.create(
            start_date='2024-04-10',
            cost=100,
            moderator=self.moderator,
            methodist=self.methodist,
            is_published=True
        )
        self.courses = [self.course_unpublished, self.course_published]

    def test_get_queryset_authenticated_user(self):
        url = reverse('courses-list')

        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        serializer = BaseCourseSerializer(self.courses, many=True)
        response_course_data = response.data.get('data')
        self.assertEquals(serializer.data, response_course_data)

    def test_get_queryset_unauthenticated_user(self):
        self.client.logout()
        url = reverse('courses-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        serializer = BaseCourseSerializer([self.course_published], many=True)
        response_course_data = response.data.get('data')
        self.assertEquals(serializer.data, response_course_data)

    def test_create_course(self):
        url = reverse('courses-list')
        data = {
            'start_date': datetime.date.today() + datetime.timedelta(days=1),
            'cost': 100,
            'methodist': self.methodist.pk,
        }

        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))
        response_course_data: dict = response.data.get('data')

        self.assertEquals(response_course_data.get('moderator'), self.moderator.pk)
        self.assertEquals(response_course_data.get('methodist'), self.methodist.pk)

    def test_retrieve_course(self):
        url = reverse('courses-detail', args=(self.course_unpublished.pk,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        serializer = BaseCourseSerializer(self.course_unpublished)
        response_course_data = response.data.get('data')
        self.assertEquals(serializer.data, response_course_data)

    def test_update_course(self):
        url = reverse('courses-detail', args=(self.course_unpublished.pk,))
        data = {
            'title': 'Test title',
            'description': 'Test description',
            'start_date': datetime.date.today() + datetime.timedelta(days=2),
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        updated_course = Course.objects.get(pk=self.course_unpublished.pk)
        serializer = UpdateCourseSerializer(updated_course)
        response_course_data = response.data.get('data')
        self.assertEquals(serializer.data, response_course_data)

    def test_partial_update_course(self):
        url = reverse('courses-detail', args=(self.course_unpublished.pk,))
        data = {
            'title': 'Test title(partial_update)'
        }
        response = self.client.put(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIsNotNone(response.data.get('data'))

        updated_course = Course.objects.get(pk=self.course_unpublished.pk)
        serializer = UpdateCourseSerializer(updated_course)
        response_course_data = response.data.get('data')
        self.assertEquals(serializer.data, response_course_data)

    def test_destroy_course(self):
        url = reverse('courses-detail', args=(self.course_unpublished.pk,))
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn('error', response.data)
        self.assertIsNone(response.data.get('error'))

        self.assertIn('message', response.data)
        self.assertIsNotNone(response.data.get('message'))
        response_course_message = response.data.get('message')
        self.assertEquals(response_course_message, 'Курс был успешно удален.')



