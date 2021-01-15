from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True, verbose_name='Аватар',
                               default='/user_avatars/4x4.jpg')
    # age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    birthday = models.DateField(verbose_name='День рождения', default=timezone.now)
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(default=(timezone.now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        return timezone.now() > self.activation_key_expires

