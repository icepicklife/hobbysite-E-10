from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction, ProductType
from .forms import ProductForm, TransactionForm

class ProductTypeListView(ListView):
    model = ProductType
    template_name = "product_type_list.html"
    context_object_name = "product_types"

    def get_queryset(self):
        # List all product types with their associated products
        return ProductType.objects.prefetch_related('products').all()

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        # Separate the user's products from the general products list
        user_products = Product.objects.filter(owner=user)
        all_products = Product.objects.exclude(owner=user)
        return {
            'user_products': user_products,
            'all_products': all_products,
        }

class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transaction_form'] = TransactionForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        # Check if the logged-in user is trying to buy their own product
        if product.owner == request.user:
            return redirect('product-list')  # Redirect if the user tries to buy their own product

        # Handle transaction creation
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save()
            # Update product stock
            product.stock -= transaction.amount
            product.save()
            return redirect('cart-view' if request.user.is_authenticated else 'login')  # Redirect based on login status
        return self.render_to_response({'transaction_form': form})

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Set the owner as the logged-in user
        return kwargs

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("product-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Ensure that the logged-in user is set
        return kwargs

    def form_valid(self, form):
        # Automatically update the status if stock is 0
        if form.instance.stock == 0:
            form.instance.status = 'Out of stock'
        return super().form_valid(form)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "cart_view.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user, status='On cart')

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(product__owner=self.request.user)
