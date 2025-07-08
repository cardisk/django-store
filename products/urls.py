from django.urls import path
from .views import ProductsView, ProductDetailsView

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name='product_list'),
    path('<slug:category_slug>', ProductsView.as_view(), name='product_list_filtered'),

    path('products/<slug:product_slug>', ProductDetailsView.as_view(), name='product_details'),
]