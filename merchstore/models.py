from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Product Types"

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("On sale", "On sale"),
        ("Out of stock", "Out of stock"),
    ]

    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )
    owner = models.ForeignKey(
        "user_management.Profile",
        on_delete=models.CASCADE,
        related_name="owned_products"
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product-detail", args=[self.pk])

    def save(self, *args, **kwargs):
        # Automatically set status to "Out of stock" if stock is 0
        if self.stock == 0:
            self.status = "Out of stock"
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("On cart", "On cart"),
        ("To Pay", "To Pay"),
        ("To Ship", "To Ship"),
        ("To Receive", "To Receive"),
        ("Delivered", "Delivered"),
    ]

    buyer = models.ForeignKey(
        "user_management.Profile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="On cart"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.pk} - {self.status}"
