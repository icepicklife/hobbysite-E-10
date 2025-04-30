from django.urls import path
from .views import (
    ProductTypeListView,
    ProductListView,  # Added the new ProductListView
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    CartView,  # Added the new CartView
    TransactionListView,  # Added the new TransactionListView
)

app_name = "merchstore"

urlpatterns = [
    path("merchstore/items", ProductTypeListView.as_view(), name="product-type-list"),
    path("merchstore/products", ProductListView.as_view(), name="product-list"),  # Updated for product list view
    path("merchstore/item/<int:pk>", ProductDetailView.as_view(), name="product-detail"),
    path("merchstore/item/add", ProductCreateView.as_view(), name="product-create"),
    path("merchstore/item/<int:pk>/edit", ProductUpdateView.as_view(), name="product-update"),
    path("merchstore/cart", CartView.as_view(), name="cart-view"),  # Updated for cart view
    path("merchstore/transactions", TransactionListView.as_view(), name="transaction-list"),  # Updated for transaction list view
]
