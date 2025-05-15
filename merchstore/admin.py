from django.contrib import admin
from .models import Product, ProductType, Transaction


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [ProductInline]
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_type", "price", "owner", "stock",
                    "status")
    list_filter = ("status", "product_type")
    search_fields = ("name", "description", "owner__user__username")

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_staff:
            return self.readonly_fields + ("product_type",)
        return self.readonly_fields


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "buyer", "amount", "status", "created_on")
    list_filter = ("status", "created_on")
    search_fields = ("product__name", "buyer__user__username")
