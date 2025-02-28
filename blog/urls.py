from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/articles', views.index, name='blog_articles'),
    path('blog/article/<int:pk>', views.index, name='blog_solo_article')
]

app_name = 'blog'
