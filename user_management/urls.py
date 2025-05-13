from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ProfileUpdateView, ProfileCreateView, post_login_redirect

app_name = "user_management"

urlpatterns = [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="user_management/login.html"),
        name="login",
    ),
    path("edit-profile/", ProfileUpdateView.as_view(), name="update_profile"),
    path("create-profile/", ProfileCreateView.as_view(), name="create_profile"),
    path("post-login-redirect/", post_login_redirect, name="post_login_redirect"),
]
