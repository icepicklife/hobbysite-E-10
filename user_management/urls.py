from django.contrib.auth import views as auth_views
from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('profile', ProfileUpdateView.as_view(), name='update_profile')
]

app_name = 'user_management'