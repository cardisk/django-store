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

    category = None

    def get_queryset(self):
        products = Product.objects.all()

        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            self.category = Category.objects.get(slug=category_slug)
            products = self.category.products.all()

        return products

    def get_context_data(self, **kwargs):
        """
        Extra data to use inside the template
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = getattr(self, 'category', None)
        return context

class ProductDetailsView(DetailView):
    """
    Product details
    """
    model = Product
    template_name = 'product_details.html'
    context_object_name = 'product'

    slug_field = 'slug'
    slug_url_kwarg = 'product_slug'
