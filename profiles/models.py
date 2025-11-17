from django.db import models
from accounts.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    skills = models.ManyToManyField('Skill')
    education = models.TextField()
    gpa = models.CharField(max_length=20)
    work_experience = models.TextField()
    links = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    
    # Privacy settings - control what recruiters can see
    profile_visible = models.BooleanField(default=True)  # Master toggle for entire profile
    headline_public = models.BooleanField(default=True)
    skills_public = models.BooleanField(default=True)
    education_public = models.BooleanField(default=True)
    gpa_public = models.BooleanField(default=True)
    work_experience_public = models.BooleanField(default=True)
    links_public = models.BooleanField(default=True)
    email_public = models.BooleanField(default=True)
    location_public = models.BooleanField(default=True)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
