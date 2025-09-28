from django.db import models
from accounts.models import User
from profiles.models import Skill
from jobs.models import Job
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #job = models.OneToOneField(Job, on_delete=models.CASCADE)



class Applicant(models.Model):
    STAGES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('hired', 'Hired'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applicants')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # optional
    stage = models.CharField(max_length=20, choices=STAGES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.post.title})"
