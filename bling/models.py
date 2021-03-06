from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .functions import how_old_is_this_datetimefield
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(default='', blank=True)
    subscribers = models.ManyToManyField(User, blank=True, default=None, verbose_name='Подписчики', related_name='Подписчик')
    friends = models.ManyToManyField(User, blank=True, default=None, verbose_name='Друзья', related_name='Друг')
    profile_image = models.OneToOneField('BlingImage', default=None, null=True, blank=True, verbose_name='Ава', on_delete=models.SET_NULL)
    liked_posts = models.ManyToManyField('BlingPost', default=None, blank=True, verbose_name='Понравившиеся посты')
    notifications_amount = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name
        else:
            return self.user.username

    def create_notification(self, sender, text, related_post=None):
        if sender == self.user:
            return 0
        elif related_post is not None:
            notification0 = BlingNotification(target_user=self.user, sender=sender, related_post=related_post, text=text)
            self.notifications_amount += 1
            notification0.save()
            self.save()
        else:
            notification0 = BlingNotification(target_user=self.user, sender=sender, text=text)
            self.notifications_amount += 1
            notification0.save()
            self.save()
        return 0

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BlingPost(models.Model):
    RENDER_LENGTH = 15
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey('BlingImage', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Изображения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор', null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    likes_amount = models.IntegerField(default=0)
    comments_amount = models.IntegerField(default=0)
    comments = models.ManyToManyField('BlingComment', default=None, blank=True, verbose_name='Комментарии')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_on']

    def how_old(self):
        return how_old_is_this_datetimefield(self.created_on)

    def __str__(self):
        if len(self.text) > self.RENDER_LENGTH:
            return self.text[:self.RENDER_LENGTH] + '...'
        else:
            return self.text


class BlingComment(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey('BlingImage', on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Изображения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор', null=True)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    likes_amount = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

    def how_old(self):
        return how_old_is_this_datetimefield(self.created_on)


class BlingImage(models.Model):
    image = models.ImageField(verbose_name='Фото', upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class BlingNotification(models.Model):
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Уведомления', verbose_name='Получатель')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    related_post = models.ForeignKey(BlingPost, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_on']

    def how_old(self):
        return how_old_is_this_datetimefield(self.created_on)