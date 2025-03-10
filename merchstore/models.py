from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Product Type"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(
        ProductType, on_delete=models.SET_NULL, null=True,
        related_name="products"
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product-detail", args=[self.pk])
