from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("threads/", views.PostListView.as_view(), name="post_list"),
    path("thread/<int:pk>/", views.PostDetailView.as_view(), name="post_view"),
]

app_name = "forum"
