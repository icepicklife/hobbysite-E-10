from django.urls import path
from .views import CombinedCreateView, ProfileUpdateView

app_name = "user_management"

urlpatterns = [
    path("create-profile/", CombinedCreateView.as_view(),
         name="create_profile"),
    path("profile/username/", ProfileUpdateView.as_view(),
         name="update_profile"),
]
