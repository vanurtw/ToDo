from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


def user_directory_path(instance, filename):
    return f'{settings.BASE_DIR}/static/users/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name='фото')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    def __str__(self):
        return f'{self.email}'


class Task(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='user_tasks',
                             verbose_name='пользователь')
    title = models.CharField(max_length=255, verbose_name='заголовок')
    description = models.TextField(verbose_name='описание')
    data_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    color_code = models.CharField(max_length=255, verbose_name='цвет')
    data_completed = models.DateField(verbose_name='указанная дата')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
