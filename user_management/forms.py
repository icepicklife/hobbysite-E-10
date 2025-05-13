from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "user_email"]
