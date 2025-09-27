from django.db import models
from accounts.models import User
from profiles.models import Skill
from recruiters.models import Post
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('review', 'Review'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('closed', 'Closed'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
