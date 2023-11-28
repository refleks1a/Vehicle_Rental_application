from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main.urls')),
    path('auth/', include('custom_auth.urls')),
    path('payment/', include('payment.urls')),
    path('cars/', include('cars.urls')),

    #path('social-auth/', include('social_django.urls', namespace='social')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'main.views.custom_404'
