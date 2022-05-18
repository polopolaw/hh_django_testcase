from django.urls import path
from stripe_api import views

urlpatterns = [
    path('buy/<int:pk>', views.buy),
    path('order/', views.order_buy),
    path('order/add', views.add_to_order),
    path('order/list', views.order_list),
    path('item/<int:pk>', views.ItemDetail.as_view()),
]
