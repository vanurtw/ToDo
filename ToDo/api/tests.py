from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser, Task
from django.shortcuts import get_object_or_404
from django.urls import reverse


# Create your tests here.


class UserTest(TestCase):

    def test_user_register(self):
        user_model = get_user_model()
