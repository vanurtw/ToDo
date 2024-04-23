from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.


def user_directory_path(instance, filename):
    return f'{settings.BASE_DIR}/static/users/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return f'{self.id}_{self.username}'
