# Generated by Django 4.2.6 on 2023-11-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_carbooking_additional_driver_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbooking',
            name='payment_success',
            field=models.BooleanField(default=False),
        ),
    ]
