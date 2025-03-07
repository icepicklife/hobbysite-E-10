from django.urls import path
from .views import ProductListView, ProductDetailView

app_name = "merchstore"

urlpatterns = [
    path("merchstore/items/", 
         ProductListView.as_view(), 
         name="product-list"),
    path("merchstore/item/<int:pk>/", 
         ProductDetailView.as_view(), 
         name="product-detail"),
]
