from django import forms
from .models import CarBooking
from phone_field import PhoneFormField, PhoneWidget


class CarBookingForm(forms.ModelForm):
    class Meta:
        model = CarBooking

        fields = ['booked_from', 'booked_to', 'milage',
                  'protection', 'additional_driver', 'infant_seat',
                  'baby_stroller', 'fuel_service', 'customer_name',
                  'customer_surname', 'customer_phone', 'country',
                  'city', 'state', 'zip', 'street', 'other_information'
                  ]

        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'firstName'}),
            'customer_surname': forms.TextInput(attrs={'class': 'form-control', 'id': 'lastName'}),
            'customer_phone': PhoneWidget(attrs={'class': 'customer_phone_input', 'id': 'customer_phone'}),

            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'state'}),
            'zip': forms.TextInput(attrs={'class': 'form-control', 'id': 'zip'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'id': 'street'}),

            'booked_from': forms.DateInput(attrs={'class': 'date_input', 'id': 'booked_from', 'type': 'date'}),
            'booked_to': forms.DateInput(attrs={'class': 'date_input', 'id': 'booked_to',  'type': 'date'}),

            'additional_driver': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'additional_driver'}),
            'infant_seat': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'infant_seat'}),
            'baby_stroller': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'baby_stroller'}),
            'fuel_service': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'fuel_service'}),

            'other_information': forms.TextInput(attrs={'class': 'form-control', 'id': 'other_information'})
        }
