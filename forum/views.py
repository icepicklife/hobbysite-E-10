from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import models
from . import forms

class ThreadListView(ListView):
    model = models.Thread
    template_name = "thread_list.html"
    context_object_name = "unused_threads_queryset"

    def get_queryset(self):
        return models.Thread.objects.select_related("category", "author").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        if self.request.user.is_authenticated:
            user_profile = get_object_or_404(models.Profile, user=self.request.user)
            user_threads = queryset.filter(author=user_profile).order_by("-created_on")
            other_threads = queryset.exclude(author=user_profile).order_by("category__name", "title")
        else:
            user_threads = None
            other_threads = queryset.order_by("category__name", "title")

        threads_by_category = {}
        for thread in other_threads:
            category_name = thread.category.name if thread.category else "Uncategorized"
            threads_by_category.setdefault(category_name, []).append(thread)

        context["user_threads"] = user_threads
        context["threads_by_category"] = threads_by_category
        context["create_thread_url"] = reverse_lazy("forum:thread_create")

        return context


class ThreadDetailView(DetailView):
    model = models.Thread
    template_name = "thread_view.html"
    context_object_name = "thread"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()

        context["more_by_author"] = models.Thread.objects.filter(
            author=thread.author).exclude(id=thread.id)[:2]
        
        if self.request.user.is_authenticated:
            context["comment_form"] = forms.CommentForm()
        
        context["forum_comments"] = thread.forum_comments.order_by("-created_on")
        context["can_edit"] = self.request.user == thread.author.user
        context["image_gallery"] = getattr(thread, "gallery_images", None)

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if not request.user.is_authenticated:
            return redirect("login")
        
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(comment_form = form)
        return self.render_to_response(context)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = models.Thread
    fields = ["title", "entry", "image", "category"]
    template_name = "Thread_form.html"
    success_url = reverse_lazy("forum:thread_list")

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Thread
    fields = ["title", "entry", "image", "category"]
    template_name = "thread_form.html"
    success_url = reverse_lazy("forum:thread_list")

    def test_func(self):
        thread = self.get_object()
        return thread.author.user == self.request.user


def index(request):
    return HttpResponse("Landing page for forum app")