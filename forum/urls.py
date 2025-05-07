from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("threads/", views.ThreadListView.as_view(), name="thread_list"),
    path("thread/<int:pk>/",views.ThreadDetailView.as_view(), name="thread_view"),
    path("thread/add/",views.ThreadCreateView.as_view(),name="thread_create"),
    path("thread/<int:pk>/edit/",views.ThreadUpdateView.as_view(),name="thread_update"),
]

app_name = "forum"