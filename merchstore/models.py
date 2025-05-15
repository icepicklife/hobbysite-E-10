from django.db import models
from user_management.models import Profile
from django.urls import reverse
from django.core.exceptions import ValidationError


def get_default_profile():
    return Profile.objects.first()


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

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
        ProductType, on_delete=models.SET_NULL, null=True,
        related_name="products"
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=get_default_profile,
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Available"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product-detail", args=[self.pk])

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.stock == 0:
            self.status = "Out of stock"
        elif self.status == "Out of stock" and self.stock > 0:
            self.status = "Available"
        super().save(*args, **kwargs)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("On cart", "On cart"),
        ("To Pay", "To Pay"),
        ("To Ship", "To Ship"),
        ("To Receive", "To Receive"),
        ("Delivered", "Delivered"),
    ]
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                              null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default="On cart")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.pk} for {self.product.name}"
