from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICES = [
        ('seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')