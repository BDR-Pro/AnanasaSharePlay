# Generated by Django 4.2.7 on 2023-12-27 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0026_alter_transaction_randomnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=98231776910, unique=True),
        ),
    ]
