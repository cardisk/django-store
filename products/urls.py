from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name='product_list'),
    path('<slug:category_slug>', ProductsView.as_view(), name='product_list_filtered'),

    path('products/<slug:product_slug>', ProductDetailsView.as_view(), name='product_details'),

    path('manage/products/', ManagementProductListView.as_view(), name='manage_product_list'),
    path('manage/products/new/', ProductCreateView.as_view(), name='product_create'),
    path('manage/products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('manage/products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('manage/categories/', ManagementCategoryListView.as_view(), name='manage_category_list'),
    path('manage/categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('manage/categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('manage/categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]