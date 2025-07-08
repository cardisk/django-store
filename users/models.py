from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds a manager flag and other profile information.
    """
    street_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Address"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="City"
    )
    postal_code = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="CAP"
    )
    is_manager = models.BooleanField(
        'Manager status',
        default=False,
        help_text='Designates whether the user is a manager and can access certain parts of the site.'
    )

    def __str__(self):
        return self.username