# Generated by Django 4.2.7 on 2023-12-29 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0044_alter_transaction_randomnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='isRated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=459738589400, unique=True),
        ),
    ]