from django.db import models

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']  # Sort categories by name (ascending)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True, blank=True)
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_on = models.DateTimeField(auto_now=True)  # Update on every save

    class Meta:
        ordering = ['-created_on']  # Sort articles by creation date (descending)

    def __str__(self):
        return self.title
