from django.urls import path
from .views import PostDetailView, PostListView

urlpatterns = [
    path('threads/', PostListView.as_view(), name='post-list'),
    path('thread/<int:pk>/', PostDetailView.as_view(), name='post-detail') 
]

app_name = 'forum'