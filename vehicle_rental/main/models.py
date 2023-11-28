from django.db import models
from custom_auth.models import CustomUser
from cars.models import Car
from phone_field import PhoneField


class CarBooking(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)

    booked_from = models.DateField()
    booked_to = models.DateField()

    MILAGE = [
        ('LD', 'Long Distance'),
        ('R', 'Regular'),
    ]

    PROTECTION = [
        ('MinE', '0'),
        ('MaxE', '300'),
        ('RedE', '150'),
        ('NotE', 'None'),
    ]

    protection = models.CharField(choices=PROTECTION, max_length=30)
    milage = models.CharField(choices=MILAGE, max_length=30)

    additional_driver = models.BooleanField(default=False)
    infant_seat = models.BooleanField(default=False)
    baby_stroller = models.BooleanField(default=False)
    fuel_service = models.BooleanField(default=False)

    customer_name = models.CharField(max_length=127)
    customer_surname = models.CharField(max_length=127)
    customer_phone = PhoneField(help_text='Phone number')

    country = models.CharField(max_length=255)
    city = models.CharField(max_length=127)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=31)
    street = models.CharField(max_length=255)

    other_information = models.TextField(max_length=511, blank=True, null=True, help_text='Might be blank')

    payment_success = models.BooleanField(default=False, editable=True)

    def get_total(self):
        return self.car.price * (self.booked_to - self.booked_from).days
