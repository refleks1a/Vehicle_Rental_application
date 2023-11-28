from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.models import CarBooking

import paypalrestsdk
from django.conf import settings


paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})


@login_required
def payment_checkout(request, booking_id):
    booking = CarBooking.objects.get(pk=booking_id)
    discount = booking.car.discount

    payment_amount = ((booking.booked_to - booking.booked_from).days * booking.car.price + booking.car.deposit) * (100 - discount)/100

    if booking.additional_driver:
        payment_amount += 50
    elif booking.infant_seat:
        payment_amount += 30
    elif booking.baby_stroller:
        payment_amount += 30
    elif booking.fuel_service:
        payment_amount += 40

    if booking.protection == 'MaxE':
        payment_amount += 300
    elif booking.protection == 'RedE':
        payment_amount += 150

    context = {
        'booking': booking,
        'payment_amount': payment_amount
    }
    return render(request, 'payment/payment.html', context)


@login_required
def create_payment(request):
    booking_id = request.GET.get('booking_id')

    booking = CarBooking.objects.get(pk=booking_id)
    discount = booking.car.discount

    payment_amount = ((booking.booked_to - booking.booked_from).days * booking.car.price + booking.car.deposit) * (100 - discount)/100

    if booking.additional_driver:
        payment_amount += 50
    elif booking.infant_seat:
        payment_amount += 30
    elif booking.baby_stroller:
        payment_amount += 30
    elif booking.fuel_service:
        payment_amount += 40

    if booking.protection == 'MaxE':
        payment_amount += 300
    elif booking.protection == 'RedE':
        payment_amount += 150

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('payment:execute_payment', kwargs={'pk': booking_id})),
            "cancel_url": request.build_absolute_uri(reverse('payment:payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": str(payment_amount),
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)
    else:
        booking.delete()
        return render(request, 'payment/payment_failed.html')


@login_required
def execute_payment(request, pk):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return payment_success(request, pk)
    else:
        return payment_failed(request)


@login_required
def payment_failed(request):
    CarBooking.objects.filter(customer=request.user).last().delete()
    return render(request, 'payment/payment_failed.html')


@login_required
def payment_success(request, pk):
    booking = CarBooking.objects.get(pk=pk)

    booking.payment_success = True
    booking.save()
    return render(request, 'payment/payment_success.html')
