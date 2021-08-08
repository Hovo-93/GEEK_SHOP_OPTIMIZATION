from django.urls import path
from ordersapp import views

app_name = 'ordersapp'

urlpatterns = [
    path('', views.OrderList.as_view(), name='orders_list'),
    path('create/', views.OrderItemCreate.as_view(), name='order_create'),
    path('read/<pk>/', views.OrderList.as_view(), name='order_read'),
    path('update/<pk>/', views.OrderList.as_view(), name='order_update'),
    path('delete/<pk>/', views.OrderList.as_view(), name='order_delete'),
]
