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

        if self.request.user.is_authenticated:
            user_articles = self.get_queryset().filter(
                author=self.request.user).order_by("-created_on")
            all_articles = self.get_queryset().exclude(
                author=self.request.user).order_by("category__name","title")
            
            articles_by_category = {}
            
            for article in all_articles:
                if article.category.name not in articles_by_category:
                    articles_by_category[article.category.name] = []
                articles_by_category[article.category.name].append(article)
            
            context['user_articles'] = user_articles
            context['articles_by_category'] = articles_by_category
            context['create_article_url'] = reverse_lazy('blog:article_create')
        else:
            articles_by_category = {}
            all_articles = self.get_queryset().order_by('category')

            for article in all_articles:
                if article.category.name not in articles_by_category:
                    articles_by_category[article.category.name] = []
                articles_by_category[article.category.name].append(article)
            
            context['articles_by_category'] = articles_by_category
            context['create_article_url'] = reverse_lazy('blog:article_create')

        
        return context


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

