# Generated by Django 4.2.7 on 2023-12-29 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0045_transaction_israted_alter_transaction_randomnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=29609453329, unique=True),
        ),
    ]
