# Generated by Django 4.2.6 on 2023-10-29 18:49

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbooking',
            name='additional_driver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='baby_stroller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='city',
            field=models.CharField(default=None, max_length=127),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='country',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='customer_name',
            field=models.CharField(default=None, max_length=127),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='customer_phone',
            field=phone_field.models.PhoneField(default=0, help_text='Phone number', max_length=31),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='customer_surname',
            field=models.CharField(default=None, max_length=127),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='fuel_service',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='infant_seat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='milage',
            field=models.CharField(choices=[('LD', 'Long Distance'), ('R', 'Regular')], default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='other_information',
            field=models.TextField(blank=True, help_text='Might be blank', max_length=511, null=True),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='protection',
            field=models.CharField(choices=[('MinE', '0'), ('MaxE', '300'), ('RedE', '150'), ('NotE', 'None')], default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='street',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carbooking',
            name='zip',
            field=models.CharField(default=0, max_length=31),
            preserve_default=False,
        ),
    ]
