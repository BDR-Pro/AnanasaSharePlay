# Generated by Django 4.2.7 on 2023-12-22 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0012_userprofile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='header',
            field=models.ImageField(default='header/default.png', upload_to='header/'),
        ),
    ]
