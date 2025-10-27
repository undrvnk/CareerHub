from django.db import models
from accounts.models import User
from profiles.models import Skill
#from jobs.models import Job
from django.contrib import admin
import csv
from django.http import HttpResponse
from io import StringIO

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    salary_range = models.CharField(max_length=100)
    required_skills = models.ManyToManyField(Skill)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    VISA_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    visa_sponsorship = models.CharField(max_length=3, choices=VISA_CHOICES, default='no')
    #job = models.OneToOneField(Job, on_delete=models.CASCADE)
    @property
    def has_location_pin(self):
        return self.lat is not None and self.lng is not None



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

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'description', 'location', 'salary_range', #'required_skills',
                    'recruiter', 'created_at', 'updated_at', 'visa_sponsorship')
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = StringIO()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in ['id', 'required_skills', "lat", "lng"]]
        writer = csv.writer(f)
        writer.writerow(['Title', 'Company', 'Description', 'Location', 'Salary Range', #'Required Skills',
                    'Recruiter', 'Created At', 'Updated At', 'Visa Sponsorship'])
        for job in queryset:
            writer.writerow([getattr(job, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=posts.csv'
        return response
    
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'stage', 'applied_at')
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = StringIO()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name != 'resume']
        writer = csv.writer(f)
        writer.writerow(['Post', 'Name', 'Email', 'Stage', 'Applied At'])
        for application in queryset:
            writer.writerow([getattr(application, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=applicants.csv'
        return response

class SavedSearch(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    skill = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result_count = models.IntegerField()
    new_results = models.IntegerField()