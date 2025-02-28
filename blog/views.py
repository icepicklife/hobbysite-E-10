from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from . import models

# Create your views here.


def index(request):
    return HttpResponse("Landing page")


def article_list(request):
    article_list = models.Article.objects.all()
    ctx = {'article': article_list}

    return render(request, "blog/article_list.html", ctx)


def article(request, pk):
    article = models.Article.objects.get(pk=pk)
    ctx = {'article': article}

    return render(request, 'blog/article_view.html', ctx)


class ArticleListView(ListView):
    model = models.Article
    template_name = 'blog/article_list.html'


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = "blog/article_view.html"
