from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("articles/", views.ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/",
         views.ArticleDetailView.as_view(), name="article_view"),
]

app_name = "blog"
