import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import CarBooking, Car
from .forms import CarBookingForm

from cars.models import Category, Class

from payment.views import payment_checkout


def contact(request):
    return render(request, 'main/contact.html')


def protection_details(request):
    return render(request, 'main/protection_details.html')


@login_required
def bookings(request):
    data = {}
    for booking in CarBooking.objects.filter(customer=request.user):
        if booking.payment_success:
            data[booking] = (booking.booked_to - booking.booked_from).days * booking.car.price + booking.car.deposit

            if booking.additional_driver:
                data[booking] += 50
            elif booking.infant_seat:
                data[booking] += 30
            elif booking.baby_stroller:
                data[booking] += 30
            elif booking.fuel_service:
                data[booking] += 40

            if booking.protection == 'MaxE':
                data[booking] += 300
            elif booking.protection == 'RedE':
                data[booking] += 150

    context = {
        'data': data,
    }
    return render(request, 'main/user_bookings.html', context)


def home(request):
    cars = Car.objects.all()
    categories = Category.objects.all()
    classes = Class.objects.all()

    if request.user.is_authenticated:
        bookings = CarBooking.objects.filter(customer=request.user)
        for book in bookings:
            if not book.payment_success:
                book.delete()

    location_input = request.GET.get('location') or ''
    booked_from_input = request.GET.get('booked_from') or ''
    booked_to_input = request.GET.get('booked_to') or ''

    if request.GET:
        return search_output(request, location_input, booked_from_input, booked_to_input)

    context = {
        'cars': cars,
        'categories': categories,
        'classes': classes,
    }
    return render(request, 'main/home.html', context)


def search_output(request, location_input, booked_from_input, booked_to_input):
    cars = []
    not_found_message = ''
    error_message = ''

    if not location_input and not booked_from_input and not booked_to_input:
        cars = Car.objects.all()

    elif location_input and booked_from_input and booked_to_input:
        for car in Car.objects.filter(location__icontains=location_input):
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if not ((datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') < datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')
                         and datetime.datetime.strptime(booked_to_input, '%Y-%m-%d') < datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')) or
                        (datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') > datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d')
                         and datetime.datetime.strptime(booked_to_input, '%Y-%m-%d') > datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d'))):

                    flag = False
            if flag and booked_to_input > booked_from_input:
                cars.append(car)

    elif location_input and booked_from_input and not booked_to_input:
        for car in Car.objects.filter(location__icontains=location_input):
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if (datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d') >= datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') >=
                        datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')):
                    flag = False
            if flag:
                cars.append(car)

    elif location_input and not booked_from_input and booked_to_input:
        for car in Car.objects.filter(location__icontains=location_input):
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if (datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d') <= datetime.datetime.strptime(booked_to_input, '%Y-%m-%d') <=
                        datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')):
                    flag = False
            if flag:
                cars.append(car)

    elif location_input and not booked_from_input and not booked_to_input:
        cars = Car.objects.filter(location__icontains=location_input)

    elif not location_input and booked_from_input and booked_to_input:
        for car in Car.objects.all():
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if not ((datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') < datetime.datetime.strptime(
                        str(booking.booked_from), '%Y-%m-%d')
                         and datetime.datetime.strptime(booked_to_input, '%Y-%m-%d') < datetime.datetime.strptime(
                            str(booking.booked_from), '%Y-%m-%d')) or
                        (datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') > datetime.datetime.strptime(
                            str(booking.booked_to), '%Y-%m-%d')
                         and datetime.datetime.strptime(booked_to_input, '%Y-%m-%d') > datetime.datetime.strptime(
                                    str(booking.booked_to), '%Y-%m-%d'))):
                    flag = False
            if flag and booked_to_input > booked_from_input:
                cars.append(car)

    elif not location_input and booked_from_input and not booked_to_input:
        for car in Car.objects.all():
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if (datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d') >= datetime.datetime.strptime(booked_from_input, '%Y-%m-%d') >=
                        datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')):
                    flag = False
            if flag:
                cars.append(car)

    elif not location_input and not booked_from_input and booked_to_input:
        for car in Car.objects.all():
            flag = True
            for booking in CarBooking.objects.filter(car=car):
                if (datetime.datetime.strptime(str(booking.booked_to), '%Y-%m-%d') <= datetime.datetime.strptime(
                        booked_to_input, '%Y-%m-%d') <=
                        datetime.datetime.strptime(str(booking.booked_from), '%Y-%m-%d')):
                    flag = False
            if flag:
                cars.append(car)

    else:
        not_found_message = 'No cars matching your search criteria'

    if booked_from_input and booked_to_input:
        if (datetime.datetime.strptime(booked_from_input, '%Y-%m-%d')) >= (datetime.datetime.strptime(booked_to_input, '%Y-%m-%d')):
            error_message = 'Book from cannot be ahead of book to'
            return render(request, 'main/invalid_search.html', {'error_message': error_message})
        elif ((datetime.datetime.strptime(booked_from_input, '%Y-%m-%d')) < datetime.datetime.now()
              or (datetime.datetime.strptime(booked_to_input, '%Y-%m-%d')) < datetime.datetime.now()):
            error_message = 'One of the entered dates are in the past'
            error_message_additional = '(Car have to be booked at least one day ahead)'
            return render(request, 'main/invalid_search.html',
                          {'error_message': error_message, 'error_message_additional': error_message_additional})
    elif booked_from_input:
        if (datetime.datetime.strptime(booked_from_input, '%Y-%m-%d')) < datetime.datetime.now():
            error_message = 'Book from is in the past'
            error_message_additional = '(You should book cars at least 1 day ahead)'
            return render(request, 'main/invalid_search.html',
                          {'error_message': error_message, 'error_message_additional': error_message_additional})
    elif booked_to_input:
        if (datetime.datetime.strptime(booked_to_input, '%Y-%m-%d')) < datetime.datetime.now():
            error_message = 'Book from is in the past'
            error_message_additional = '(You should book cars at least 1 day ahead)'
            return render(request, 'main/invalid_search.html',
                          {'error_message': error_message, 'error_message_additional': error_message_additional})

    context = {
        'cars': cars,
        'location': location_input,
        'booked_from': booked_from_input,
        'booked_to': booked_to_input,
        'not_found_message': not_found_message,
    }

    return render(request, 'main/search_cars.html', context)


class CarBook(LoginRequiredMixin, FormView):
    login_url = 'custom_auth:login'
    success_url = reverse_lazy('main:home')

    form_class = CarBookingForm
    template_name = 'main/book_car.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.request.GET.get('car_id')

        context['car'] = Car.objects.get(pk=car_id)

        return context

    def form_valid(self, form):
        car_id = self.request.GET.get('car_id')
        car = Car.objects.get(pk=car_id)

        booking = form.save(commit=False)
        bookings = CarBooking.objects.filter(car=car)

        if not self.request.user.email_is_verified:
            booking.delete()
            return redirect(reverse_lazy('main:home'))

        flag = True

        for book in bookings:
            if not ((booking.booked_from < book.booked_from and booking.booked_to < book.booked_from) or
                    (booking.booked_from > book.booked_to and booking.booked_to > book.booked_to)):
                flag = False

        if self.request.user.email_is_verified and self.request.user.is_active and flag and booking.booked_from < booking.booked_to:
            car.car_booked_to = booking.booked_to
            car.car_booked_from = booking.booked_from

            booking.customer = self.request.user
            booking.car = car

            booking.save()
            car.save()
            return payment_checkout(self.request, booking.id)

        return super().form_valid(form)


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)
