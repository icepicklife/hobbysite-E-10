from django.urls import path
from . import views

urlpatterns = [
    path('threads/', views.ThreadListView.as_view(), name='thread_list'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_view') 
]

app_name = 'forum'