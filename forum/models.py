from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ThreadCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Thread Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("forum:category_detail", args=[str(self.pk)])


class Thread(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, related_name="threads"
    )
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ThreadCategory, on_delete=models.SET_NULL,
        null=True, related_name="threads"
    )
    entry = models.TextField()
    image = models.ImageField(
        upload_to="thread_images/", blank=True,
        null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forum:thread_view", args=[str(self.pk)])


class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, related_name="forum_comments"
    )
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="forum_comments"
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.entry[:50]
