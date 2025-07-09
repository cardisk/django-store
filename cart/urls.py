from django.urls import path
from .views import CartAddView, CartRemoveView, CartDetailView

app_name = 'cart'

urlpatterns = [
    path('list/', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
]