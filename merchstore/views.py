from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product, ProductType


class ProductListView(ListView):
    model = ProductType
    template_name = "product_list.html"
    context_object_name = "product_types"

    def get_queryset(self):
        return ProductType.objects.prefetch_related("products").all()


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


def product_list(request):
    product_types = ProductType.objects.prefetch_related("products").all()
    ctx = {"product_types": product_types}

    return render(request, "product_list.html", ctx)


def product_detail(request, pk):
    ctx = {"product": Product.objects.get(pk=pk)}

    return render(request, "product_detail.html", ctx)
