from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models


class ArticleListView(ListView):
    model = models.Article
    template_name = "blog/article_list.html"
    context_object_name = "all_articles"

    def get_queryset(self):
        return models.Article.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = "blog/article_view.html"


def index(request):
    return HttpResponse("Landing page for blog app")


def article_list(request):
    article_list = models.Article.objects.all()
    ctx = {"article": article_list}

    return render(request, "blog/article_list.html", ctx)


def article(request, pk):
    article = models.Article.objects.get(pk=pk)
    ctx = {"article": article}

    return render(request, "blog/article_view.html", ctx)

