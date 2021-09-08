from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    born_on = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    friend_requests = models.ManyToManyField(User, blank=True, default=None, verbose_name='Подписчики', related_name='Подписчик')
    friends = models.ManyToManyField(User, blank=True, default=None, verbose_name='Друзья', symmetrical=True, related_name='Друг')
    profile_image = models.ImageField(default=None, verbose_name='Ава')

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
