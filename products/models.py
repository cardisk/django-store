from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """
    Categories
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Automatically generated slug from the name"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    """
    A product inside the store
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Product Name"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        help_text="Automatically generated slug from the name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock quantity"
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="Product Image"
    )
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL, # If category is eliminated, the product is not removed
        null=True,
        blank=True, # Optional
        verbose_name="Category"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)