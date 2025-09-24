from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    firstname = models.CharField(max_length=150, blank=True)
    lastname = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    ROLE_CHOICES = [
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')