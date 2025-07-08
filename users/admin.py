from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {
            'fields': (
                'is_manager',
                'street_address',
                'city',
                'postal_code',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile', {
            'fields': (
                'is_manager',
                'street_address',
                'city',
                'postal_code',
            ),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_manager', 'city')
    list_filter = UserAdmin.list_filter + ('is_manager', 'city',)

admin.site.register(User, CustomUserAdmin)