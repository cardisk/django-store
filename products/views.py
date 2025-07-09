from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from users.mixins import ManagerRequiredMixin
from .models import Product, Category
from .forms import ProductForm, CategoryForm

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

class ManagementProductListView(ManagerRequiredMixin, ListView):
    model = Product
    template_name = 'management/product_list.html'
    context_object_name = 'products'

class ProductCreateView(ManagerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'management/product_form.html'
    success_url = reverse_lazy('products:manage_product_list')

    def form_valid(self, form):
        messages.success(self.request, "Product created successfully.")
        return super().form_valid(form)

class ProductUpdateView(ManagerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'management/product_form.html'
    success_url = reverse_lazy('products:manage_product_list')

    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully.")
        return super().form_valid(form)

class ProductDeleteView(ManagerRequiredMixin, DeleteView):
    model = Product
    template_name = 'management/product_confirm_delete.html'
    success_url = reverse_lazy('products:manage_product_list')

    def form_valid(self, form):
        messages.success(self.request, "Product deleted successfully.")
        return super().form_valid(form)

class ManagementCategoryListView(ManagerRequiredMixin, ListView):
    model = Category
    template_name = 'management/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(ManagerRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'management/category_form.html'
    success_url = reverse_lazy('products:manage_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)

class CategoryUpdateView(ManagerRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'management/category_form.html'
    success_url = reverse_lazy('products:manage_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

class CategoryDeleteView(ManagerRequiredMixin, DeleteView):
    model = Category
    template_name = 'management/category_confirm_delete.html'
    success_url = reverse_lazy('products:manage_category_list')

    def form_valid(self, form):
        messages.success(self.request, "Category deleted successfully.")
        return super().form_valid(form)
