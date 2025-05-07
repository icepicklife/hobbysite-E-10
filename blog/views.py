from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from . import forms

class ArticleListView(ListView):
    model = models.Article
    template_name = "blog/article_list.html"
    context_object_name = "unused_articles_queryset"

    def get_queryset(self):
        return models.Article.objects.select_related("category", "author").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        if self.request.user.is_authenticated:
            user_profile = get_object_or_404(models.Profile, user=self.request.user)
            user_articles = queryset.filter(author=user_profile).order_by("-created_on")
            other_articles = queryset.exclude(author=user_profile).order_by("category__name", "title")
        else:
            user_articles = None
            other_articles = queryset.order_by("category__name", "title")

        articles_by_category = {}
        for article in other_articles:
            category_name = article.category.name if article.category else "Uncategorized"
            articles_by_category.setdefault(category_name, []).append(article)

        context["user_articles"] = user_articles
        context["articles_by_category"] = articles_by_category
        context["create_article_url"] = reverse_lazy("blog:article_create")

        return context


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = "blog/article_view.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        context["more_by_author"] = models.Article.objects.filter(
            author=article.author).exclude(id=article.id)[:2]
        
        if self.request.user.is_authenticated:
            context["comment_form"] = forms.CommentForm()
        
        context["comments"] = article.comments.order_by("-created_on")
        context["can_edit"] = self.request.user == article.author.user
        context["image_gallery"] = getattr(article, "gallery_images", None)

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            return redirect("login")
        
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(comment_form = form)
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = models.Article
    fields = ["title", "entry", "header", "category"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Article
    fields = ["title", "entry", "header", "category"]
    template_name = "blog/article_form.html"
    success_url = reverse_lazy("blog:article_list")

    def test_func(self):
        article = self.get_object()
        return article.author.user == self.request.user


def index(request):
    return HttpResponse("Landing page for blog app")

