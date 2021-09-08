from django.db import models
from userprofile.models import UserProfile


class BlingPost(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    images = models.ForeignKey('BlingImage', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Изображения')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    liked_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Понравилось')
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
    image = models.ImageField(verbose_name='Фото')
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, verbose_name='Владелец')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
