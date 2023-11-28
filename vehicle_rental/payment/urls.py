from django.urls import path

from .views import create_payment, execute_payment, payment_failed, payment_success

app_name = 'payment'

urlpatterns = [
    path('create_payment/', create_payment, name='create_payment'),
    path('execute_payment/<int:pk>', execute_payment, name='execute_payment'),
    path('payment_failed/', payment_failed, name='payment_failed'),
    path('payment_success/', payment_success, name='payment_success'),
]