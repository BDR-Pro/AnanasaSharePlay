# Generated by Django 4.2.7 on 2023-12-20 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0009_game_genre_alter_game_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='games',
            field=models.ManyToManyField(blank=True, default=None, related_name='user_games', to='shareplay.game'),
        ),
    ]
