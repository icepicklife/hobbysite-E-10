from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.


def index(request):
    return HttpResponse("Landing page")


def thread_list(request):
    thread_list = models.Post.objects.all()
    ctx = {'thread': thread_list}

    return render(request, "forum/thread_list.html", ctx)


def thread(request, pk):
    thread = models.Post.objects.get(pk=pk)
    ctx = {'thread': thread}

    return render(request, 'forum/thread_view.html', ctx)


class ThreadListView(ListView):
    model = models.Post
    template_name = 'forum/thread_list.html'


class ThreadDetailView(DetailView):
    model = models.Post
    template_name = "forum/thread_view.html"