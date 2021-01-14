from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True, verbose_name='Аватар')
    # age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    birthday = models.DateField(verbose_name='День рождения', default=timezone.now)
