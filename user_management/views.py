from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileForm
    template_name = "profile_form.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ["user_email", "display_name"]
    template_name = "create_profile.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# Create your views here.
