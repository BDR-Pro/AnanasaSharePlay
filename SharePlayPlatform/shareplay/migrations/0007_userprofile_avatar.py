# Generated by Django 4.2.7 on 2023-12-19 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0006_remove_userprofile_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatar/default.png', upload_to='avatar/'),
        ),
    ]