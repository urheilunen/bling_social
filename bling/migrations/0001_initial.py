# Generated by Django 3.2.5 on 2021-09-30 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('born_on', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('friends', models.ManyToManyField(blank=True, default=None, related_name='Друг', to=settings.AUTH_USER_MODEL, verbose_name='Друзья')),
                ('profile_image', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bling.blingimage', verbose_name='Ава')),
                ('subscribers', models.ManyToManyField(blank=True, default=None, related_name='Подписчик', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='BlingPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('images', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bling.blingimage', verbose_name='Изображения')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='BlingComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('images', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bling.blingimage', verbose_name='Изображения')),
                ('related_post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bling.blingpost', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
