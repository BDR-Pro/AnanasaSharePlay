# Generated by Django 4.2.7 on 2024-01-01 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0054_alter_transaction_listid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='owners',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=339214576132, unique=True),
        ),
    ]