from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('created/', OrderCreatedView.as_view(), name='order_created'),

    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

    path('manage/', ManagementOrderListView.as_view(), name='manage_order_list'),
    path('manage/<int:pk>/complete/', OrderMarkCompletedView.as_view(), name='order_complete'),
    path('manage/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]