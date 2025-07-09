from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib import messages
from products.models import Product
from .cart import Cart

class CartAddView(LoginRequiredMixin, View):
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
        messages.success(request, f'{product.name} added to the cart')
        return redirect(redirect_url)

    def get(self, request, *args, **kwargs):
        """
        Handles the redirect from the login page.
        The user was trying to add an item, but had to log in first.
        We can't re-add the item as the POST data is lost.
        """
        messages.info(request, "You are now logged in. Please try adding the item to your cart again.")
        return redirect('products:product_list')


class CartRemoveView(LoginRequiredMixin, View):
    """
    Remove a product from the shopping cart
    Only POST requests are handled.
    """
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(LoginRequiredMixin, TemplateView):
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