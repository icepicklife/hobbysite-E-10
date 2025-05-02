from django.urls import path
from .views import ArticleListView, ArticleDetailView
from django.conf import settings
from django.conf.urls.static import static

app_name = "wiki"

urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article_list"),
    path("article/<int:pk>/", ArticleDetailView.as_view(),name="article_detail"),
    # path("article/add/"),
    # path("article/<int:pk>/edit/")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
