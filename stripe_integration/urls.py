from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stripe_api.urls')),
    path('', include('stripe_front.urls'))
]
