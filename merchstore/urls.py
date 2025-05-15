from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    CartView,
    TransactionListView,
)

app_name = "merchstore"

urlpatterns = [
    path("merchstore/items", ProductListView.as_view(), name="product-list"),
    path(
        "merchstore/item/<int:pk>", ProductDetailView.as_view(),
        name="product-detail"
    ),
    path("merchstore/item/add", ProductCreateView.as_view(),
         name="product-create"),
    path(
        "merchstore/item/<int:pk>/edit",
        ProductUpdateView.as_view(),
        name="product-update",
    ),
    path("merchstore/cart", CartView.as_view(), name="cart-view"),
    path(
        "merchstore/transactions",
        TransactionListView.as_view(),
        name="transaction-list",
    ),
]
