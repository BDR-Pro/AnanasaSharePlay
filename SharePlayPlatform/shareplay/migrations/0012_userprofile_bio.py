# Generated by Django 4.2.7 on 2023-12-22 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0011_userprofile_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
