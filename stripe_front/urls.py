from django.urls import path
from stripe_front import views

urlpatterns = [
    path('', views.index),
]
