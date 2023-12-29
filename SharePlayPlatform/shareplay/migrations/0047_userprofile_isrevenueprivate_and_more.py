# Generated by Django 4.2.7 on 2023-12-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareplay', '0046_userprofile_revenue_alter_transaction_randomnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='isRevenuePrivate',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='randomNumber',
            field=models.IntegerField(default=27265862694, unique=True),
        ),
    ]