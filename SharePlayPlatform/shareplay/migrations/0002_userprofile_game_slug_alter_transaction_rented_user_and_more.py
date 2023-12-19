# Generated by Django 4.2.7 on 2023-12-19 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shareplay', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('nickname', models.CharField(max_length=255)),
                ('for_rent', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='rented_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='games',
            field=models.ManyToManyField(to='shareplay.game'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
