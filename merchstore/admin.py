from django.contrib import admin
from .models import Product, ProductType


class ProductInline(admin.TabularInline):
    model = Product


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "price")


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
