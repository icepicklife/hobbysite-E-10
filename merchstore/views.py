from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Transaction
from .forms import ProductForm, TransactionForm
from user_management.models import Profile 
from accounts.models import UserAccount
from django.contrib import messages
from django.http import HttpResponseRedirect

class ProductListView(ListView): 
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"  

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            profile, created = Profile.objects.get_or_create(user=user)
            user_products = Product.objects.filter(owner=profile)
            all_products = Product.objects.exclude(owner=profile)
        else:
            user_products = None
            all_products = Product.objects.all()
        
        return user_products, all_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_products, all_products = self.get_queryset()

        context['user_products'] = user_products
        context['all_products'] = all_products

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        user = self.request.user

        context['is_owner'] = user.is_authenticated and product.owner == user.profile

        context['transaction_form'] = TransactionForm(
            user=user if user.is_authenticated else None,
            initial={'product': product}
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        form = TransactionForm(request.POST, user=request.user if request.user.is_authenticated else None)

        if not request.user.is_authenticated:
            request.session['pending_transaction'] = {
                'product_id': product.pk,
                'amount': request.POST.get('amount'),
            }
            messages.info(request, "Please log in to complete your transaction.")
            return redirect(f"{reverse('accounts:login')}?next={request.path}")

        if form.is_valid():
            transaction = form.save(commit=False)

            try:
                profile = Profile.objects.get(user=request.user)
                transaction.buyer = profile
            except Profile.DoesNotExist:
                messages.error(request, "Your account does not have a profile. Please contact support.")
                return redirect('accounts:profile')

            transaction.status = 'On cart'
            transaction.save()
            messages.success(request, "Added to cart.")
            return redirect('merchstore:cart-view')

        context = self.get_context_data(object=self.object)
        context['transaction_form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        # Check for post-login transaction in session
        pending = request.session.pop('pending_transaction', None)
        if request.user.is_authenticated and pending:
            product = get_object_or_404(Product, pk=pending['product_id'])

            try:
                profile = Profile.objects.get(user=request.user)
                Transaction.objects.create(
                    product=product,
                    buyer=profile,
                    amount=pending['amount'],
                    status='On cart'
                )
                messages.success(request, "Your transaction was added after login.")
                return redirect('merchstore:cart-view')
            except Profile.DoesNotExist:
                messages.error(request, "Your account does not have a profile. Please contact support.")
                return redirect('accounts:profile')

        return super().get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("merchstore:product-list")

    def form_valid(self, form):
        try:
            form.instance.owner = self.request.user.profile  # from user_management
        except Profile.DoesNotExist:
            messages.error(self.request, "You need a profile to create a product.")
            return redirect("accounts:profile")  # Adjust as needed
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("merchstore:product-list")

    def form_valid(self, form):
        try:
            profile = self.request.user.profile  # from user_management
        except Profile.DoesNotExist:
            messages.error(self.request, "You need a profile to update a product.")
            return redirect("accounts:profile")

        if self.get_object().owner != profile:
            messages.error(self.request, "You are not authorized to edit this product.")
            return redirect("merchstore:product-list")

        if form.instance.stock == 0:
            form.instance.status = 'Out of stock'
        else:
            form.instance.status = 'Available'

        return super().form_valid(form)

class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "cart_view.html"
    context_object_name = "transactions"

    def get_queryset(self):
        try:
            profile = self.request.user.profile
            return Transaction.objects.filter(
                buyer=profile,
                status='On cart'
            ).select_related('product__owner').order_by('product__owner__user__username')
        except Profile.DoesNotExist:
            return Transaction.objects.none()

class TransactionListView(LoginRequiredMixin, TemplateView):
    template_name = "transaction_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            context['transactions_grouped'] = []
            return context

        transactions = Transaction.objects.filter(product__owner=profile).select_related('buyer__user', 'product')

        buyer_groups = {}
        for tx in transactions:
            buyer = tx.buyer
            if buyer not in buyer_groups:
                buyer_groups[buyer] = []
            buyer_groups[buyer].append(tx)

        context['transactions_grouped'] = sorted(buyer_groups.items(), key=lambda x: x[0].user.username)
        return context
