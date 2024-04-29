from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser, Task
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.


class UserTest(TestCase):

    def setUp(self) -> None:
        user_model = get_user_model()
        user = user_model.objects.create(username='test',
                                         email='test@test.ru',
                                         password='awdawdawWdwas',
                                         first_name='test',
                                         last_name='test')
        self.user = user
        self.client = APIClient()
        self.client.force_authenticate(user)

    def test_user_register(self):
        user_model = get_user_model()
        url = reverse('users')
        data = {
            'username': 'user',
            'password': 'userawdawWA',
            'email': 'awdW@awd.awd',
        }
        self.assertEqual(user_model.objects.count(), 1)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_model.objects.count(), 2)

    def test_user_serializer(self):
        user_model = get_user_model()
        user = user_model.objects.create(username='user',
                                         email='user@user.ru',
                                         password='awdawdawWdwas',
                                         first_name='test',
                                         last_name='test')
        data = {
            'id': user.id,
            'email': 'user@user.ru',
        }
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data, data)

    def test_users_get(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
