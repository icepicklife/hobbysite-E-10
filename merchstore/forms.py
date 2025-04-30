from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'description', 'price', 'stock', 'status']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'amount', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Set the buyer field to the logged-in user if provided
            self.fields['buyer'].initial = user
            self.fields['buyer'].widget.attrs['readonly'] = True  # Make the buyer field readonly
