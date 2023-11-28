from django.urls import path
from .views import CarsByCategory, CarsByClass, CarDetailView

app_name = 'cars'

urlpatterns = [
    path('category/<int:pk>', CarsByCategory.as_view(), name='category'),
    path('class/<int:pk>', CarsByClass.as_view(), name='class'),
    path('car/<int:pk>', CarDetailView.as_view(), name='detail'),
]