from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.


def index(request):
    return HttpResponse("Landing page for forum app")


def thread_list(request):
    thread_list = models.Post.objects.all()
    ctx = {"thread": thread_list}

    return render(request, "forum/post_list.html", ctx)


def thread(request, pk):
    thread = models.Post.objects.get(pk=pk)
    ctx = {"thread": thread}

    return render(request, "forum/post_view.html", ctx)


class PostListView(ListView):
    model = models.Post
    template_name = "post_list.html"


class PostDetailView(DetailView):
    model = models.Post
    template_name = "post_view.html"
