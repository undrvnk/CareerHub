from django.db import models
from accounts.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    skills = models.ManyToManyField('Skill')
    education = models.TextField()
    work_experience = models.TextField()
    links = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
