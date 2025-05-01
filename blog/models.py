from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Article Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category_detail", args=[str(self.pk)])


class Article(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.SET_NULL,
        null=True, related_name="articles")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ArticleCategory, on_delete=models.SET_NULL,
        null=True, related_name="articles")
    entry = models.TextField()
    header = models.ImageField(upload_to="article_headers/",null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article_view", args=[str(self.pk)])
    

class Comment(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.SET_NULL,
        null=True, related_name="comments")
    article = models.ForeignKey(Article,
        on_delete=models.CASCADE, 
        related_name="comments")
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return self.entry[:50]
