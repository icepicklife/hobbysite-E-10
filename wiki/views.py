from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Article
from accounts.models import UserAccount


class ArticleListView(ListView):
    model = Article
    template_name = "wiki/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return super().get_queryset().order_by("category__name", "title", "-created_on")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            try:
                profile = UserAccount.objects.get(user=user)
                user_articles = Article.objects.filter(author=profile)
                other_articles = Article.objects.exclude(author=profile)
            except UserAccount.DoesNotExist:
                user_articles = None
                other_articles = Article.objects.all()
            
            context["user_articles"] = user_articles
            context["all_articles"] = other_articles
        else:
            context["user_articles"] = None
            context["all_articles"] = Article.objects.all()

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "wiki/article_detail.html"
    context_object_name = "article"
