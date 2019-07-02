from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('orders', views.orders_list, name = 'orders_list'),
    path('order/create/', views.order_create, name = 'order_create')
]
