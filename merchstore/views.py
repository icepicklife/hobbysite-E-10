from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"


def product_list(request):
    products = Product.objects.all()
    ctx = {"products": products}

    return render(request, "product_list.html", ctx)


def recipe_detail(request, pk):
    ctx = {"product": Product.objects.get(pk=pk)}

    return render(request, "product_detail.html", ctx)
