from django.urls import path
from .views import home, CarBook, payment_checkout, contact, bookings, protection_details


app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('bookings/', bookings, name='bookings'),

    path('book_car/<int:pk>/', CarBook.as_view(), name='book_car'),
    path('book_car/car_payment/<int:pk>', payment_checkout, name='car_payment'),

    path('protection_info/', protection_details, name='protection_details')
]
