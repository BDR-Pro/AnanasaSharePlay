# Generated by Django 4.2.7 on 2023-12-19 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0007_userprofile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=255), max_length=255, unique=True),
        ),
    ]