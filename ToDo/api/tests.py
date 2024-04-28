from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser, Task
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status


# Create your tests here.


class UserTest(TestCase):

    def test_user_register(self):
        user_model = get_user_model()
        url = reverse('register')
        data = {
            'username': 'user',
            'password': 'userawdawWA',
            'email': 'awdW@awd.awd',
        }
        self.assertEqual(user_model.objects.count(), 0)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user_model.objects.count(), 1)

    def test_user_serializer(self):
        data = {

        }
