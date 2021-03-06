# Generated by Django 3.2.5 on 2021-10-09 08:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0009_auto_20211009_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='blingnotification',
            name='created_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='blingnotification',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
