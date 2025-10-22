# jobs/models.py (Change made)
from django.db import models
from accounts.models import User
from profiles.models import Skill
from django.contrib import admin
import csv
from django.http import HttpResponse
from io import StringIO

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary_range = models.CharField(max_length=100)
    visa_sponsorship = models.CharField(max_length=200)
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
    
    job = models.ForeignKey('recruiters.Post', on_delete=models.CASCADE, default=None)    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    note = models.TextField(blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'description', 'location', 'salary_range', 'visa_sponsorship', #'required_skills',
                    'recruiter', 'created_at', 'updated_at')
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name != 'required_skills']
        f = StringIO()

        writer = csv.writer(f)
        writer.writerow(['Title', 'Company', 'Description', 'Location', 'Salary Range', 'Visa Sponsorship', #'Required Skills',
                    'Recruiter', 'Created At', 'Updated At'])
        for job in queryset:
            writer.writerow([getattr(job, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=jobs.csv'
        return response
    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'note', 'created_at', 'updated_at')
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(['Job', 'Applicant', 'Status', 'Note', 'Created At', 'Updated At'])
        for application in queryset:
            writer.writerow([getattr(application, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applications.csv'
        return response