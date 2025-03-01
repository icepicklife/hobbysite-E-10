from django.db import models
from django.urls import reverse

# Create your models here.


class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Post Categories'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('forum:category_detail', args=[str(self.pk)])
    
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        PostCategory, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='post'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:post_view', args=[str(self.pk)])

