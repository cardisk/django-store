from unicodedata import category

from django.views.generic import ListView, DetailView
from .models import Product, Category

class ProductsView(ListView):
    """
    List of products
    """
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.all()

        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category_query = Category.objects.get(slug=category_slug)
            products = category_query.products.all()

        return products

class ProductDetailsView(DetailView):
    """
    Product details
    """
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
