# Generated by Django 4.2.7 on 2023-12-19 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0002_userprofile_game_slug_alter_transaction_rented_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='slug',
        ),
    ]
