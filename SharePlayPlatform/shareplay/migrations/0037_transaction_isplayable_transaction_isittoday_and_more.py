# Generated by Django 4.2.7 on 2023-12-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0036_ratestreamer_game_alter_ratestreamer_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='isPlayable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='isitToday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=544282977635, unique=True),
        ),
    ]
