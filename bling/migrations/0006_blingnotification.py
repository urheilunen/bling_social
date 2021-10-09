# Generated by Django 3.2.5 on 2021-10-08 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bling', '0005_auto_20211006_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlingNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_seen', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('text', models.TextField()),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Уведомления', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
    ]