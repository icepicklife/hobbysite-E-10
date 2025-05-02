from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('user_management:update_profile')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


# Create your views here.
