from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "user_email"]

    def __init__(self, *args, disable_email=False, **kwargs):
        super().__init__(*args, **kwargs)
        if disable_email:
            self.fields["user_email"].disabled = True

