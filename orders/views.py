from django.shortcuts import redirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart

class OrderCreateView(FormView):
    """
    Order creation.
    """
    template_name = 'create.html'
    form_class = OrderCreateForm

    def dispatch(self, request, *args, **kwargs):
        """
        Stops the checkout page if cart is empty
        """
        cart = Cart(request)
        if not cart:
            messages.warning(request, "Your cart is empty. You cannot proceed to checkout.")
            return redirect('products:product_list')
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Pre-fill the user fields
        """
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['first_name'] = self.request.user.first_name
            initial['last_name'] = self.request.user.last_name
            initial['email'] = self.request.user.email
            initial['address'] = self.request.user.street_address
            initial['postal_code'] = self.request.user.postal_code
            initial['city'] = self.request.user.city
        return initial

    def get_context_data(self, **kwargs):
        """
        Add the cart to the context
        """
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context

    def form_valid(self, form):
        """
        Only when form data is valid.
        Order logic.
        """
        cart = Cart(self.request)

        try:
            with transaction.atomic():
                order = form.save(commit=False)
                if self.request.user.is_authenticated:
                    order.user = self.request.user
                order.save()

                for item in cart:
                    product = item['product']

                    if product.stock < item['quantity']:
                        raise ValueError(f"Not enough stock for {product.name}.")

                    # 3. Crea gli OrderItem
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=item['price'],
                        quantity=item['quantity']
                    )

                    product.stock -= item['quantity']
                    product.save(update_fields=['stock'])
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

        cart.clear()

        self.request.session['order_id'] = order.id
        return redirect(self.get_success_url())

    def get_success_url(self):
        """
        Next url for redirect
        """
        return reverse('orders:order_created')


class OrderCreatedView(TemplateView):
    """
    Confirmation page after checkout
    """
    template_name = 'created.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        if order_id:
            try:
                context['order'] = Order.objects.get(id=order_id)
            except Order.DoesNotExist:
                context['order'] = None
        return context