from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job, Application

class Pipeline(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class PipelineStage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    stage = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
