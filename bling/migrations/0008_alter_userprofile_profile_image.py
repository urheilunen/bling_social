# Generated by Django 3.2.5 on 2021-09-22 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bling', '0007_alter_blingimage_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='bling.blingimage', verbose_name='Ава'),
        ),
    ]