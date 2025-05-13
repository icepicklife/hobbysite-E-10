from django import forms
from .models import Product, Transaction

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['product', 'amount', 'status', 'buyer']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            self.fields['buyer'].initial = user
            self.fields['buyer'].widget.attrs['readonly'] = True  # Make the field readonly for logged-in users
        else:
            # If not authenticated, remove 'buyer' from form fields to avoid the KeyError
            del self.fields['buyer']

