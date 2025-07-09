from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Allows editing OrderItems directly within the Order admin page.
    """
    model = OrderItem
    # Use raw_id_fields for product selection to avoid slow-loading dropdowns
    # if you have many products.
    raw_id_fields = ['product']
    readonly_fields = ('price', 'get_cost',)
    # Don't show extra empty forms
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Order model.
    """
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'completed',
        'created'
    ]
    list_editable = ['completed']
    list_filter = ['completed', 'created', 'updated']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'created', 'updated', 'get_total_cost')

    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Total Cost'