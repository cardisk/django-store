from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, ListView, DetailView, DeleteView, View
from users.mixins import ManagerRequiredMixin
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm

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

class OrderListView(LoginRequiredMixin, ListView):
    """
    Display the list of orders for the current user.
    """
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """
        Return only the orders for the currently logged-in user.
        """
        return Order.objects.filter(user=self.request.user).order_by('-created')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Display the details of a specific order.
    """
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        """
        Ensure the user can only view their own orders.
        This is a crucial security measure.
        """
        return Order.objects.filter(user=self.request.user)


class ManagementOrderListView(ManagerRequiredMixin, ListView):
    model = Order
    template_name = 'management/order_list.html'
    context_object_name = 'orders'
    ordering = ['-created']

class OrderMarkCompletedView(ManagerRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.completed = True
        order.save()
        messages.success(request, f"Order #{order.id} has been marked as completed.")
        return redirect('orders:manage_order_list')

class OrderDeleteView(ManagerRequiredMixin, DeleteView):
    model = Order
    template_name = 'management/order_confirm_delete.html'
    success_url = reverse_lazy('orders:manage_order_list')

    def form_valid(self, form):
        messages.success(self.request, f"Order #{self.object.id} has been deleted.")
        return super().form_valid(form)