from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from . import models


def article_list(request):
    article_list = models.Article.objects.all()
    ctx = {'articles': article_list}  

    return render(request, "wiki/article_list.html", ctx)


def article(request, pk):
    article = models.Article.objects.get(pk=pk)
    ctx = {'article': article}

    return render(request, 'wiki/article_detail.html', ctx)


class ArticleListView(ListView):
    model = models.Article
    template_name = "wiki/article_list.html"
    context_object_name = "articles"

class ArticleDetailView(DetailView):
    model = models.Article
    template_name = "wiki/article_detail.html"
    context_object_name = "article"
