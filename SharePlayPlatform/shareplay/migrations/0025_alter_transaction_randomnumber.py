# Generated by Django 4.2.7 on 2023-12-27 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0024_transaction_randomnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=508775571972),
        ),
    ]
