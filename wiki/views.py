from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, Comment, ArticleCategory
from .forms import (
    ArticleCreateForm,
    ArticleUpdateForm,
    CommentForm,
    ArticleCategoryCreateForm,
)
from user_management.models import Profile


class ArticleListView(ListView):
    model = Article
    template_name = "wiki/article_list.html"

    def get_queryset(self):
        return super().get_queryset().order_by("category__name", "title", "-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            try:
                profile = Profile.objects.get(user=user)
                user_articles = Article.objects.filter(author=profile)
                other_articles = Article.objects.exclude(author=profile)
            except Profile.DoesNotExist:
                user_articles = None
                other_articles = Article.objects.all()

            context["user_articles"] = user_articles
            context["all_articles"] = other_articles
        else:
            context["user_articles"] = None
            context["all_articles"] = Article.objects.all()

        return context

    def get_success_url(self):
        return reverse("wiki:article_list", kwargs={"pk": self.object.pk})


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = "wiki/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("wiki:article_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        context["related_articles"] = Article.objects.filter(
            category=article.category
        ).exclude(pk=article.pk)

        context["comments"] = article.comment_set.order_by("-created_on")
        context["form"] = self.get_form()

        user = self.request.user
        context["is_owner"] = (
            user.is_authenticated
            and hasattr(user, "profile")
            and article.author == user.profile
        )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            if request.user.is_authenticated and hasattr(request.user, "profile"):
                comment = form.save(commit=False)
                comment.article = self.object
                comment.author = request.user.profile
                comment.save()
                return redirect(self.get_success_url())
            else:
                return redirect("login")
        else:
            return self.form_invalid(form)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = "wiki/article_create.html"
    success_url = reverse_lazy("wiki:article_list")

    # for category creation
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_form"] = ArticleCategoryCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        category_form = ArticleCategoryCreateForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect("wiki:article_create")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect("USERS ONLY")
        form.instance.author = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("wiki:article_list")


class ArticleCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ArticleCategory
    form_class = ArticleCategoryCreateForm
    template_name = "wiki/article_category_create.html"
    success_url = reverse_lazy("wiki:article_create")

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleUpdateForm
    template_name = "wiki/article_update.html"

    def get_success_url(self):
        return reverse("wiki:article_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect("USERS ONLY")
        form.instance.author = profile
        return super().form_valid(form)
