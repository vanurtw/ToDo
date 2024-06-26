from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import CustomUser, Task
from django.urls import reverse
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, TaskSerializer
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.


class UserTest(TestCase):

    def setUp(self) -> None:
        user_model = get_user_model()
        user = user_model.objects.create_user(username='test',
                                              email='test@test.ru',
                                              password='awdawdawWdwas',
                                              first_name='test',
                                              last_name='test')
        self.user = user
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user)

    def test_user_register(self):
        self.client.logout()
        self.token.delete()
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
        token_qs = Token.objects.all()
        self.assertEqual(token_qs.count(), 1)
        user = user_model.objects.get(email=data.get('email'))
        token = Token.objects.get(user=user)
        data_response = {
            'auth_token': token.key
        }
        self.assertEqual(response.data, data_response)

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

    def test_users_patch(self):
        url = reverse('users')
        new_email = 'user@user.ru'
        self.assertNotEqual(self.user.email, new_email)
        response = self.client.patch(url, data={'email': new_email})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(self.user.email, new_email)

    def test_register_error(self):
        self.client.logout()
        url = reverse('users')
        data = {'email': 'test@test.ru', 'password': 'awdsadawdawdaw'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'user@user.ru', }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'email': 'test@test.ru', 'password': 'test'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    def test_users_error_get(self):
        self.client.logout()
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_users_error_patch(self):
        get_user_model().objects.create_user(email='user@user.ru', password='awdawdaw', username='user')
        url = reverse('users')
        data = {'email': 'user@user.ru'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_auth_login(self):
        self.client.logout()
        self.token.delete()
        url = reverse('djoser:login')
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 0)
        user = get_user_model().objects.all()[0]
        data = {'email': 'test@test.ru', 'password': 'awdawdawWdwas'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=user)
        data = {'auth_token': token.key}
        self.assertEqual(response.data, data)
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 1)

    def test_users_auth_logout(self):
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 1)
        url = reverse('djoser:logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 0)

    def test_users_auth_lgin_error(self):
        self.client.logout()
        self.token.delete()
        url = reverse('djoser:login')
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 0)
        user = get_user_model().objects.all()[0]
        data = {'email': 'error', 'password': 'awdawdawWdwas'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 0)
        data = {'email': 'test@test.ru', 'password': 'error'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        tokens = Token.objects.all()
        self.assertEqual(tokens.count(), 0)


class TaskTest(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()
        user = user_model.objects.create_user(username='user', email='user@user.ru', password='awdawdwadwarb')
        token = Token.objects.create(user=user)
        self.user = user
        self.token = token
        task = Task.objects.create(title='test',
                                   description='test',
                                   color_code='test',
                                   data_completed='1990-03-27',
                                   tag='test',
                                   user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)


def test_tasks_get(self):
    url = reverse('tasks')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    url = reverse('tasks') + '?date=1990/03/27'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    url = reverse('tasks') + '?date=2000/06/21'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 0)
    url = reverse('tasks') + '?tag=test'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    url = reverse('tasks') + '?tag=test_test'
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 0)


def test_tasks_post(self):
    url = reverse('tasks')
    data = {
        'title': 'new_task',
        'description': 'new_task',
        'color_code': 'color_new',
        'tag': 'new_task',
        'data_completed': '2002-11-05'
    }
    response = self.client.post(url, data=data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    tasks = Task.objects.filter(title='new_task',
                                description='new_task',
                                color_code='color_new',
                                tag='new_task').exists()
    self.assertTrue(tasks)


def test_tasks_serializer(self):
    task = Task.objects.create(user=self.user,
                               title='new_task',
                               description='new_task',
                               color_code='color_new',
                               tag='new_task',
                               data_completed='2002-11-05'
                               )
    data = {'id': task.id,
            'user': self.user.id,
            'title': 'new_task',
            'description': 'new_task',
            'color_code': 'color_new',
            'data_completed': '2002-11-05',
            'completed': False,
            'tag': 'new_task'
            }
    serializer = TaskSerializer(task)
    self.assertEqual(serializer.data, data)


def test_tasks_error(self):
    self.client.logout()
    self.token.delete()
    url = reverse('tasks')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    data = {
        'title': 'new_task',
        'description': 'new_task',
        'color_code': 'color_news',
        'data_completed': '2002-11-05',
        'tag': 'new_task'
    }
    response = self.client.post(url, data=data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    task = Task.objects.filter(title='new_task',
                               description='new_task',
                               color_code='color_news',
                               tag='new_task').exists()
    self.assertFalse(task)


class TaskDetail(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        user = get_user_model().objects.create_user(username='test',
                                                    password='test',
                                                    email='test@test.ru')
        self.user = user
        token = Token.objects.create(user=user)
        self.token = token
        self.client.force_authenticate(self.user)
        task = Task.objects.create(user=self.user,
                                   title='test',
                                   description='test',
                                   color_code='test',
                                   data_completed='1990-05-11',
                                   tag='test')
        self.task = task

    def test_task_detail_get(self):
        url = reverse('task_detail', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_task_detail_path(self):
        url = reverse('task_detail', kwargs={'id': 1})
        data = {'title': 'new_task', 'tag': 'new_task', 'completed': True}
        self.assertNotEqual(self.task.title, data['title'])
        self.assertNotEqual(self.task.tag, data['tag'])
        self.assertNotEqual(self.task.completed, data['completed'])
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.get(id=1)
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.tag, data['tag'])
        self.assertEqual(task.completed, data['completed'])

    def test_task_detail_delete(self):
        id = 1
        task = Task.objects.filter(id=id)
        self.assertTrue(task.exists())
        url = reverse('task_detail', kwargs={'id': id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task = Task.objects.filter(id=id)
        self.assertFalse(task.exists())

    def test_task_detail_error_no_auth(self):
        self.client.logout()
        url = reverse('task_detail', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_detail_error_get(self):
        user_new = get_user_model().objects.create_user(username='new_user',
                                                        password='awdwawdaawdwad',
                                                        email='new_user@new.ru')
        task = Task.objects.create(user=user_new,
                                   title='new',
                                   description='new',
                                   color_code='new',
                                   data_completed='1995-05-11',
                                   tag='test')
        url = reverse('task_detail', kwargs={'id': task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
