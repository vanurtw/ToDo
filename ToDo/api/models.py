from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


def user_directory_path(instance, filename):
    return f'{settings.BASE_DIR}/static/users/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return f'{self.username}'


class Task(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='user_tasks',
                             blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    data_create = models.DateTimeField(auto_now_add=True)
    color_code = models.CharField(max_length=255)
    data_completed = models.DateTimeField()

    def __str__(self):
        return self.title
