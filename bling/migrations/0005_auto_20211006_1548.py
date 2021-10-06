# Generated by Django 3.2.5 on 2021-10-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0004_profile_liked_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blingcomment',
            name='related_post',
        ),
        migrations.AddField(
            model_name='blingpost',
            name='comments',
            field=models.ManyToManyField(blank=True, default=None, to='bling.BlingComment', verbose_name='Комментарии'),
        ),
    ]