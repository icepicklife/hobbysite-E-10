from django.db import models
from django.urls import reverse

class Commission(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    people_req = models.BigIntegerField()
    date_created_on = models.DateTimeField(auto_now_add=True)
    date_updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["date_created_on"]
    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('commission:commissions_detail', args=[self.pk])


class Comment(models.Model):

    commission = models.ForeignKey(
        
        Commission,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    entry = models.TextField()
    date_created_on = models.DateTimeField(auto_now_add=True)
    date_updated_on = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ["-date_created_on"]


    def __str__(self):
        return f"Comment on {self.commission.title}"

# Create your models here.

