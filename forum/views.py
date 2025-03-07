from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, PostCategory

# Create your views here.

def thread_list(request):
    thread_lists = (PostCategory.objects.prefetch_related("post").all())
    ctx = {'thread_lists': thread_lists}

    return render(request, "post_list.html", ctx)


def thread(request, pk):
    threads = Post.objects.get(pk=pk)
    ctx = {'thread': threads}

    return render(request, 'post_detail.html', ctx)


class PostListView(ListView):
    model = PostCategory
    template_name = 'post_list.html'
    context_object_name = "thread_lists"

    def get_queryset(self):
        return PostCategory.objects.prefetch_related("post").all()


class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
