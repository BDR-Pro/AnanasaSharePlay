# Generated by Django 4.2.7 on 2023-12-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0016_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ending_time',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_time',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
