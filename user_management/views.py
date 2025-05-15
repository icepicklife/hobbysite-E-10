from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from .models import Profile
from .forms import ProfileForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class CombinedCreateView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = ProfileForm()
        return render(
            request,
            "create_profile.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )

    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect("index")

        return render(
            request,
            "create_profile.html",
            {
                "user_form": user_form,
                "profile_form": profile_form,
            },
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profile_update.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return self.request.user.profile
