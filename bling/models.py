from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    born_on = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    subscribers = models.ManyToManyField(User, blank=True, default=None, verbose_name='Подписчики', related_name='Подписчик')
    friends = models.ManyToManyField(User, blank=True, default=None, verbose_name='Друзья', symmetrical=True, related_name='Друг')
    profile_image = models.OneToOneField('BlingImage', default=None, null=True, blank=True, verbose_name='Ава', on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.user

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class BlingPost(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey('BlingImage', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Изображения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор', null=True)
    liked_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='Понравилось')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_on']


class BlingComment(BlingPost):
    related_post = models.OneToOneField(BlingPost, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class BlingImage(models.Model):
    image = models.ImageField(verbose_name='Фото', upload_to='images/')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
