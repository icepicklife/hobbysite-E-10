from django.contrib.auth import views as auth_views
from django.urls import path
from .views import CombinedCreateView, ProfileUpdateView

app_name = "user_management"

urlpatterns = [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="user_management/login.html"),
        name="login",
    ),
    path("create-profile/", CombinedCreateView.as_view(), name="create_profile"),
    path("profile/username/", ProfileUpdateView.as_view(), name="update_profile"),
]
