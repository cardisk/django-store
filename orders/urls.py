from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('created/', OrderCreatedView.as_view(), name='order_created'),

    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]