from django.db import models


class BlingUser(models.Model):
    nickname = models.CharField(max_length=30, verbose_name='Никнейм')
    name = models.CharField(max_length=30, verbose_name='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия')
    created_on = models.DateField(auto_now_add=True, verbose_name='Дата регистрации')
    born_on = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    friend_requests = models.ManyToManyField('self', null=True, blank=True, default=None, verbose_name='Подписчики')
    friends = models.ManyToManyField('self', null=True, blank=True, default=None, verbose_name='Друзья')
    profile_image = models.ForeignKey('BlingImage', on_delete=models.PROTECT, blank=True, null=True, default=None, verbose_name='Фото')
    email = models.EmailField(null=True, blank=True, verbose_name='E-mail')

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['surname']

    def __str__(self):
        return self.nickname


class BlingPost(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name='Текст')
    images = models.ManyToManyField('BlingImage', null=True, blank=True, verbose_name='Изображения')
    author = models.ForeignKey(BlingUser, on_delete=models.PROTECT, related_name='posts', verbose_name='Автор')
    liked_by = models.ManyToManyField(BlingUser, null=True, blank=True, verbose_name='Понравилось')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_on']


class BlingComment(BlingPost):
    related_post = models.ForeignKey(BlingPost, on_delete=models.PROTECT, related_name='comments', verbose_name='Пост')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class BlingImage(models.Model):
    image = models.ImageField(verbose_name='Фото')
    owner = models.ForeignKey(BlingUser, on_delete=models.PROTECT, verbose_name='Владелец')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
