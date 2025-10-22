# profiles/admin.py
from django.contrib import admin
from .models import Profile
import csv
from django.http import HttpResponse
from io import StringIO

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'headline', 'education', 'gpa', 'work_experience', 'links', 'skills') # WANT TO INCLUDE DATE CREATED/UPDATED, MAYBE FUTURE
    list_display = ('user', 'headline', 'created_at', 'updated_at')
    search_fields = ('user__username', 'headline')
    list_filter = ('created_at', 'updated_at')
    actions = ['download_csv']
    def download_csv(self, request, queryset):
        f = StringIO()
        meta = self.model._meta
        field_names = [field.name for field in meta.fields if field.name not in ['id', 'skills']]
        writer = csv.writer(f)
        writer.writerow(['User', 'Headline', 'Educatoin', 'GPA', 'Work Experience', #'Required Skills',
                    'Links', 'Created At', 'Updated At'])
        for job in queryset:
            writer.writerow([getattr(job, field) for field in field_names])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=profiles.csv'
        return response