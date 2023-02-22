from django.contrib.auth.models import AbstractUser
from django.db import models as m


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
