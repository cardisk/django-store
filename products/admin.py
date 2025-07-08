from django.contrib import admin

from products.models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'price', 'stock', 'image', 'category']
    list_filter = ['category']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}