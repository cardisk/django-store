from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib import messages
from products.models import Product
from .cart import Cart

class CartAddView(View):
    """
    Add a product to cart or update the quantity
    Only POST requests are handled.
    """
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        quantity = int(request.POST.get('quantity', 1))

        cart.add(product=product, quantity=quantity, override_quantity=False)
        redirect_url = request.META.get('HTTP_REFERER', 'products:product_list')
        messages.success(request, 'Product[s] added to the cart')
        return redirect(redirect_url)


class CartRemoveView(View):
    """
    Remove a product from the shopping cart
    Only POST requests are handled.
    """
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(TemplateView):
    """
    Show the cart content
    """
    template_name = 'cart_details.html'
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        """
        Extra data to use inside the template
        """
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context