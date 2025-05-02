from django.db import models
from django.urls import reverse
from django.utils import timezone

from user_management.models import Profile


class Commission(models.Model):

    STATUS_STATES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
        ('Completed', 'Completed'),
        ('Discontinued', 'Discontinued'),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_STATES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True,)
    updated_on = models.DateTimeField(auto_now=True,)

    class Meta:
        ordering = ["created_on"]

    def get_absolute_url(self):
        return reverse('commission_detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Job(models.Model):

    STATUS_STATES = [
        ('Open', 'Open'),
        ('Full', 'Full'),
    ]

    commission = models.ForeignKey(Commission, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_STATES, default='Open')


    class Meta:
        ordering = ['status', '-manpower_required', 'role']


    def __str__(self):
        return f"{self.role} ({self.status})"

class JobApplication(models.Model):

    STATUS_STATES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_STATES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True,)

    
    class Meta:

        ordering = [
            models.Case(
                models.When(status='Pending', then=1),
                models.When(status='Accepted', then=2),
                models.When(status='Rejected', then=3),
                output_field=models.IntegerField()
            ),
            '-applied_on'
        ]
    
    def __str__(self):
        return f"{self.applicant.display_name} - {self.status}"

        