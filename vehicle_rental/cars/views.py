from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Car, Category, Class


class CarsByCategory(ListView):
    template_name = 'cars/category.html'
    model = Car

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        category_id = self.request.GET.get('category_id')
        car_category = Category.objects.get(pk=category_id)

        context['cars'] = Car.objects.filter(car_category=car_category)
        context['category'] = car_category

        return context


class CarsByClass(ListView):
    template_name = 'cars/class.html'
    model = Car

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        class_id = self.request.GET.get('class_id')
        car_class = Class.objects.get(pk=class_id)

        context['cars'] = Car.objects.filter(car_class=car_class)

        return context


class CarDetailView(DetailView):
    template_name = 'cars/car_detail.html'
    model = Car
    context_object_name = 'car'

